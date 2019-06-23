from evalrescallers import mykrobe_pub_data, ten_k_validation_data


def make_samples_tsv(json_dict, outfile):
    '''Writes TSV file of all samples, which dataset they belong to,
    and their phenotypes.
    json_dict expected to be json object loaded from summary.json
    made by tb-amr-benchmarking pipeline'''
    ten_k_drugs, ten_k_pheno_data_validation, ten_k_pheno_data_test, ten_k_predict_data = ten_k_validation_data.load_all_data()
    ten_k_sources = ten_k_validation_data.load_sources_file(ten_k_validation_data.sources_file)
    ten_k_countries = {x: ten_k_sources[x][1] for x in ten_k_sources}
    myk_all_drugs, myk_sample_to_res, myk_sample_to_country = mykrobe_pub_data.load_all_nature_suppl_files('tb')
    # don't include Quinolones. It's inferred from the other drugs, and not
    # actually in the original data. The phenos are there as the separate drugs.
    myk_all_drugs.remove('Quinolones')
    ten_k_drugs.remove('Quinolones')

    all_drugs = sorted(list(ten_k_drugs.union(myk_all_drugs)))
    dictionaries = [
        ('train', myk_sample_to_res, myk_sample_to_country),
        ('validate', ten_k_pheno_data_validation, ten_k_countries),
        ('test', ten_k_pheno_data_test, ten_k_countries),
    ]
    country_counts = {}
    dataset_rename = {'train': 'training', 'validate': 'global', 'test': 'prospective'}

    with open(outfile, 'w') as f:
        print('ENA_id', 'Dataset', 'Country', *all_drugs, sep='\t', file=f)

        for dataset_name, dataset_dict, country_dict in dictionaries:
            for sample in sorted(dataset_dict):
                if sample not in json_dict:
                    continue

                country = country_dict[sample]

                phenotypes = []
                for drug in all_drugs:
                    phenotype = dataset_dict[sample].get(drug, 'U')
                    if phenotype not in {'R', 'S', 'U'}:
                        phenotype = 'U'
                    phenotypes.append(phenotype)

                print(sample, dataset_rename[dataset_name], country, *phenotypes, sep='\t', file=f)

                if country not in country_counts:
                    country_counts[country] = {'train': 0, 'validate': 0, 'test': 0}
                country_counts[country][dataset_name] += 1

    return country_counts

