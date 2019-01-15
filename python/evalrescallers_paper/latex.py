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




def mean_sens_and_spec_on_one_dataset(stats_tsv_file, tools, drugs, dataset, outfile):
    stats = {t: {x: 0 for x in ['TP', 'FP', 'TN', 'FN']} for t in tools}

    with open(stats_tsv_file) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for d in reader:
            if d['Dataset'] != dataset or d['Drug'] not in drugs or d['Tool'] not in tools:
                continue

            for x in ['TP', 'FP', 'TN', 'FN']:
                stats[d['Tool']][x] += int(d[x])


    with open(outfile, 'w') as f:
        print(r'''\begin{tabular}{lcccccc}''', file=f)
        header_fields = ['Tool'] +  [r'''\multicolumn{1}{c}{''' + x + '}' for x in ['Sensitivity', 'Specificity', 'VME', 'ME', 'PPV', 'NPV']]
        print(*header_fields, sep=' & ', end=r''' \\''' + ' \n', file=f)

        for tool, d in sorted(stats.items()):
            sensitivity = round(100 * d['TP'] / (d['TP'] + d['FN']), 2)
            specificity = round(100 * d['TN'] / (d['TN'] + d['FP']), 2)
            vme = round(100 * d['FN'] / (d['FN'] + d['TP']), 2)
            me = round(100 * d['FP'] / (d['FP'] + d['TN']), 2)
            ppv = round(100 * d['TP'] / (d['TP'] + d['FP']), 2)
            npv = round(100 * d['TN'] / ( d['TN'] + d['FN']), 2)
            print(tool, f'{sensitivity:.2f}', f'{specificity:.2f}', f'{vme:.2f}', f'{me:.2f}', f'{ppv:.2f}', f'{npv:.2f}', sep=' & ', end=r''' \\''' + ' \n', file=f)

        print(r'''\end{tabular}''', file=f)



def regimen_summary_table(regimen_summary_file, outfile, datasets, tools):
    counts = {tool: {'right': 0, 'wrong': 0} for tool in tools}

    with open(regimen_summary_file) as f:
        reader = csv.DictReader(f, delimiter='\t')

        for d in reader:
            if d['Dataset'] not in datasets or d['Tool'] not in tools or d['Truth_regimen'] == 'NA':
                continue

            assert d['Tool'] in counts
            if d['Truth_regimen'] == d['Called_regimen'] or (d['Truth_regimen'] == '10' and d['Called_regimen'] in {'10', '11', '12'}):
                key = 'right'
            else:
                key = 'wrong'

            counts[d['Tool']][key] += int(d['Count'])


    with open(outfile, 'w') as f:
        print(r'''\begin{tabular}{lrrr}''', file=f)
        print(r'''Tool & Correct regimen & Incorrect regimen & Percent correct \\''', file=f)
        print(r'''\hline''', file=f)
        for tool in sorted(list(counts)):
            percent = round(100 * counts[tool]['right'] / (counts[tool]['right'] + counts[tool]['wrong']), 1)
            print(common_data.tool_names[tool], counts[tool]['right'], counts[tool]['wrong'], percent, end=r''' \\''' + '\n', sep=' & ', file=f)

        print(r'''\hline''', file=f)
        print(r'''\end{tabular}''', file=f)


