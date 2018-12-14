import csv


def load_accuracy_stats_file(infile, dataset, tool):
    stats = {}
    with open(infile) as f:
        reader = csv.DictReader(f, delimiter='\t')

        for d in reader:
            if d['Dataset'] != dataset or d['Tool'] != tool:
                continue

            stats[d['Drug']] = d

    return stats



def get_data_for_differences_between_stats_files(infile_r_res, infile_r_susc, dataset, tool):
    r_res_data = load_accuracy_stats_file(infile_r_res, dataset, tool)
    r_susc_data = load_accuracy_stats_file(infile_r_susc, dataset, tool)
    drugs = set(r_res_data.keys()).union(set(r_susc_data.keys()))

    diffs = {}
    print('Drug', 'R_TP', 'R_TN', 'R_FP', 'R_FN', 'r_TP', 'r_TN', 'r_FP', 'r_FN', sep='\t')

    for drug in drugs:
        assert drug in r_res_data and drug in r_susc_data
        r_res_tuple = tuple([r_res_data[drug][x] for x in ['TP', 'TN', 'FP', 'FN']])
        r_susc_tuple = tuple([r_susc_data[drug][x] for x in ['TP', 'TN', 'FP', 'FN']])
        if r_res_tuple == r_susc_tuple:
            continue

        print(drug, *r_res_tuple, *r_susc_tuple, sep='\t')

    return diffs



def report_diffs_between_stats_files(infile_r_res, infile_r_susc, dataset, tool):
    diffs = get_differences_between_stats_files(infile_r_res, infile_r_susc, dataset, tool)
    # FIXME:
    # 1. MAke plots
    # 2. Make TSV file of data
    import pprint
    pprint.pprint(diffs)

