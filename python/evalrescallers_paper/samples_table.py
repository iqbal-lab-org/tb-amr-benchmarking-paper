from evalrescallers import mykrobe_pub_data, ten_k_validation_data


def make_samples_tsv(json_dict, outfile):
    '''Writes TSV file of all samples, which dataset they belong to,
    and their phenotypes.
    json_dict expected to be json object loaded from summary.json
    made by tb-amr-benchmarking pipeline'''
    ten_k_drugs, ten_k_pheno_data_validation, ten_k_pheno_data_test, ten_k_predict_data = ten_k_validation_data.load_all_data()
    myk_all_drugs, myk_sample_to_res = mykrobe_pub_data.load_all_nature_suppl_files('tb')
    # don't include Quinolones. It's inferred from the other drugs, and not
    # actually in the original data. The phenos are there as the separate drugs.
    myk_all_drugs.remove('Quinolones')

    all_drugs = sorted(list(ten_k_drugs.union(myk_all_drugs)))
    dictionaries = [
        ('training', myk_sample_to_res),
        ('validation', ten_k_pheno_data_validation),
        ('test', ten_k_pheno_data_test),
    ]

    with open(outfile, 'w') as f:
        print('ENA_id', 'Dataset', *all_drugs, sep='\t', file=f)

        for dataset_name, dataset_dict in dictionaries:
            for sample in sorted(dataset_dict):
                if sample not in json_dict:
                    continue

                phenotypes = []
                for drug in all_drugs:
                    phenotype = dataset_dict[sample].get(drug, 'U')
                    if phenotype not in {'R', 'S', 'U'}:
                        phenotype = 'U'
                    phenotypes.append(phenotype)

                print(sample, dataset_name, *phenotypes, sep='\t', file=f)

