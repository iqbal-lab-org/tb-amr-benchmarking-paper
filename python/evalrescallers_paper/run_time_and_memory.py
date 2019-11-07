import csv
import json
import os
import subprocess
import sys
import textwrap


def json_to_tsv(json_dict, tsv_out):
    '''json_dict expected to be json object loaded from summary.json
    made by tb-amr-benchmarking pipeline'''
    with open(tsv_out, 'w') as f:
        print('Sample', 'Tool', 'RAM (MB)', 'Wall_clock (s)', sep='\t', file=f)

        for sample in sorted(json_dict):
            for tool, tool_dict in sorted(json_dict[sample].items()):
                if tool != '10k_predict' and tool_dict['Success']:
                    if 'time_and_memory' in tool_dict:
                        ram_in_mb = round(tool_dict['time_and_memory']['ram'] / 1000, 2)
                        time_in_seconds = round(tool_dict['time_and_memory']['wall_clock_time'], 2)
                        print(sample, tool, ram_in_mb, time_in_seconds, sep='\t', file=f)
                    else:
                        print(f'No time_and_memory found for sample {sample} and tool {tool}', file=sys.stderr)


def tsv_to_plot(tsv_file, outprefix):
    '''Makes box plots of run time and memory,
    using TSV file made by json_to_tsv'''
    time_pdf = f'{outprefix}.time.pdf'
    memory_pdf = f'{outprefix}.memory.pdf'
    medians_csv = f'{outprefix}.medians.csv'

    r_string = r'''        library(ggplot2)
        d = read.csv(file="''' + tsv_file + r'''", sep="\t", header=T)

        ggplot(d, aes(x=Tool, y=Wall_clock..s. / 60)) +
          geom_boxplot() +
          xlab("Tool") +
          ylab("Wall clock time (m)") +
          theme_linedraw() +
          theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
          scale_y_continuous(trans='log10')
        ggsave(filename="''' + time_pdf + '''", width=6, height=5, scale=0.95)


        ggplot(d, aes(Tool, RAM..MB.)) +
          geom_boxplot() +
          xlab("Tool") +
          ylab("Peak RAM (MB)") +
          theme_linedraw() +
          theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
          scale_y_continuous(trans='log10')
        ggsave(filename="''' + memory_pdf + '''", width=6, height=5, scale=0.95)

        file.remove("Rplots.pdf")
        write.csv(aggregate(d[,3:4], list(d$Tool), median), file="''' + medians_csv + r'''")'''

    r_script = f'{outprefix}.R'
    with open(r_script, 'w') as f:
        print(textwrap.dedent(r_string), file=f)
    subprocess.check_output(f'R CMD BATCH {r_script}', shell=True)
    os.unlink(f'{r_script}out')
    try:
        os.unlink('.RData')
    except:
        pass


def csv_to_latex_table(csv_file, outfile):
    '''Makes latex table file of median run times and memory,
    from CSV file made by tsv_to_plot()'''
    ignore = {'Mykrobe.CP1', 'Mykrobe.CP2', 'Mykrobe.CP3', 'Mykrobe.Walker-2015'}

    with open(csv_file) as f_in, open(outfile, 'w') as f_out:
        reader = csv.DictReader(f_in)
        print(r'''\begin{tabular}{lrr}''', file=f_out)
        print(r'''\hline''', file=f_out)
        print(r'''Tool & RAM (MB) & Time (m) \\''', file=f_out)
        print(r'''\hline''', file=f_out)

        for d in reader:
            if d['Group.1'] in ignore:
                continue

            print(d['Group.1'], int(round(float(d['RAM..MB.']), 0)), round(float(d['Wall_clock..s.']) / 60, 1), sep=' & ', end=r''' \\''' + '\n', file=f_out)

        print(r'''\hline''', file=f_out)
        print(r'''\end{tabular}''', file=f_out)

