from collections import OrderedDict
import csv

from evalrescallers_paper import common_data


def tool_accuracy_table_on_one_dataset(stats_tsv_file, tool, drugs, dataset, outfile):
    tool_stats = {}

    with open(stats_tsv_file) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for d in reader:
            if d['Dataset'] != dataset or d['Tool'] != tool:
                continue

            assert d['Drug'] not in tool_stats
            tool_stats[d['Drug']] = OrderedDict([
                ('Drug', d['Drug']),
                ('TP', d['TP']),
                ('FP', d['FP']),
                ('TN', d['TN']),
                ('FN', d['FN']),
                ('VME (95\% CI)', f'${d["FNR"]}$(${d["FNR_conf_low"]}$-${d["FNR_conf_high"]}$\%)'),
                ('ME (95\% CI)', f'${d["FPR"]}$(${d["FPR_conf_low"]}$-${d["FPR_conf_high"]}$\%)'),
                ('PPV (95\% CI)', f'${d["PPV"]}$(${d["PPV_conf_low"]}$-${d["PPV_conf_high"]}$\%)'),
                ('NPV (95\% CI)', f'${d["NPV"]}$(${d["NPV_conf_low"]}$-${d["NPV_conf_high"]}$\%)'),
            ])

    with open(outfile, 'w') as f:
        printed_header = False

        for drug in drugs:
            if drug not in tool_stats:
                print('Drug not in tool_stats:', drug)
            assert drug in tool_stats
            if not printed_header:
                print(r'''\begin{tabular}{''', 'c' * len(tool_stats[drug]), '}', sep='', file=f)
                print(r'''\hline''', file=f)
                print(*tool_stats[drug].keys(), sep=' & ', file=f, end='')
                print(r''' \\''', file=f)
                print(r'''\hline''', file=f)
                printed_header = True

            print(*tool_stats[drug].values(), sep=' & ', file=f, end='')
            print(r''' \\''', file=f)

        print(r'''\hline''', file=f)
        print(r'''\end{tabular}''', file=f)




def regimen_summary_table(regimen_summary_file, outfile, datasets, tools):
    counts = {tool: {'right': 0, 'wrong': 0} for tool in tools}

    with open(regimen_summary_file) as f:
        reader = csv.DictReader(f, delimiter='\t')

        for d in reader:
            if d['Dataset'] not in datasets or d['Tool'] not in tools or d['Truth_regimen'] == 'NA':
                continue

            assert d['Tool'] in counts
            if d['Truth_regimen'] == d['Called_regimen']:
                key = 'right'
            else:
                key = 'wrong'

            counts[d['Tool']][key] += int(d['Count'])


    with open(outfile, 'w') as f:
        print(r'''\begin{tabular}{lrr}''', file=f)
        print(r'''Tool & Correct regimen & Incorrect regimen \\''', file=f)
        print(r'''\hline''', file=f)
        for tool in sorted(list(counts)):
            print(common_data.tool_names[tool], counts[tool]['right'], counts[tool]['wrong'], end=r''' \\''' + '\n', sep=' & ', file=f)

        print(r'''\hline''', file=f)
        print(r'''\end{tabular}''', file=f)


