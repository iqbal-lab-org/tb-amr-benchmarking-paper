import csv

from evalrescallers_paper import common_data


def load_accuracy_stats_file(infile, dataset, tool):
    stats = {}
    ints = {'TP', 'TN', 'FP', 'FN', 'FAIL_R', 'FAIL_S', 'UNK_R', 'UNK_S'}
    words = {'Dataset', 'Drug', 'Tool'}

    with open(infile) as f:
        reader = csv.DictReader(f, delimiter='\t')

        for d in reader:
            if d['Dataset'] != dataset or d['Tool'] != tool:
                continue

            for k in d:
                if k in words:
                    pass
                elif k in ints:
                    d[k] = int(d[k])
                elif d[k] == 'NA':
                    pass
                else:
                    d[k] = float(d[k])

            stats[d['Drug']] = d

    return stats


def get_data_for_differences_between_stats_files(infile_r_res, infile_r_susc, dataset, tool):
    r_res_data = load_accuracy_stats_file(infile_r_res, dataset, tool)
    r_susc_data = load_accuracy_stats_file(infile_r_susc, dataset, tool)
    drugs = set(r_res_data.keys()).union(set(r_susc_data.keys()))

    data = {}

    for drug in drugs:
        assert drug in r_res_data and drug in r_susc_data
        data[drug] = {'r': r_susc_data[drug], 'R': r_res_data[drug]}

    return data


def table_of_diffs_between_stats_files(infile_r_res, infile_r_susc, dataset, tool, outfile, drugs=None):
    data = get_data_for_differences_between_stats_files(infile_r_res, infile_r_susc, dataset, tool)

    drugs_from_diffs = sorted(list(common_data.first_line_drugs)) + sorted([x for x in data if x not in common_data.first_line_drugs.union({'Quinolones'})])
    if drugs is None:
        drugs = drugs_from_diffs
    else:
        drugs = [x for x in drugs if x in drugs_from_diffs]

    total_with_pheno = []
    total_r_calls = []
    r_fp = []
    table_data = []

    for drug in drugs:
        if drug not in data:
            continue

        total_with_pheno_r = sum([data[drug]['r'][x] for x in ['TP', 'TN', 'FP', 'FN']])
        total_with_pheno_R = sum([data[drug]['R'][x] for x in ['TP', 'TN', 'FP', 'FN']])
        assert total_with_pheno_r == total_with_pheno_R
        total_with_pheno = total_with_pheno_r
        r_fp_calls = data[drug]['R']['FP'] - data[drug]['r']['FP']
        r_tp_calls = data[drug]['R']['TP'] - data[drug]['r']['TP']
        r_all_calls = r_fp_calls + r_tp_calls
        if r_all_calls == 0:
            continue

        percent_fp = round(100 * r_fp_calls / r_all_calls, 2)

        table_data.append([
            drug,
            str(total_with_pheno),
            str(r_all_calls),
            str(percent_fp),
        ])


    with open(outfile, 'w') as f:
        print(r'''\begin{tabular}{cccc}''', file=f)
        print(r'''\hline''', file=f)
        print(r'''Drug & Samples & Minority variant calls & False-positive rate \\ ''', file=f)
        print(r'''\hline''', file=f)
        for fields in table_data:
            print(*fields, sep=' & ', end=' ', file=f)
            print(r''' \\ ''', file=f)

        print(r'''\hline''', file=f)
        print(r'''\end{tabular}''', file=f)

