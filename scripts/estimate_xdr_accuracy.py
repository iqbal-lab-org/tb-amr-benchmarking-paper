#!/usr/bin/env python3

# Used to estimate the number of correct calls, from the samples that
# were assigned MDR-TB (regimen 11) from phenotypes, but mykrobe called
# as XDR-TB. Do this using the PPV of Mfx.

import csv

dataset_lookup = {"10k_test": "prospective", "10k_validate": "global"}


def get_ppv():
    with open("r_is_resistant.accuracy_stats.tsv") as f:
        reader = csv.DictReader(f, delimiter="\t")
        drug = "Moxifloxacin"
        ppvs = {"global": None, "prospective": None}

        for row in reader:
            if row["Tool"] != "Mykrobe.201901":
                continue

            if row["Dataset"] in dataset_lookup and row["Drug"] == drug:
                dataset = dataset_lookup[row["Dataset"]]
                ppvs[dataset] = int(row["TP"]) / (int(row["TP"]) + int(row["FP"]))

    return ppvs


def get_sample_counts_regimen_11_to_12():
    counts = {x: 0 for x in dataset_lookup.values()}

    with open("r_is_resistant.regimen_counts.summary.tsv") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if (
                row["Dataset"] in dataset_lookup
                and row["Tool"] == "Mykrobe.201901"
                and row["Truth_regimen"] == "11"
                and row["Called_regimen"] == "12"
            ):
                counts[dataset_lookup[row["Dataset"]]] += int(row["Count"])

    return counts


ppv = get_ppv()
sample_counts = get_sample_counts_regimen_11_to_12()
print("PPV:", ppv)
print("Number of samples:", sample_counts)
total_samples = sum(sample_counts.values())
print("Total samples:", total_samples)
expect_correct = {d: ppv[d] * sample_counts[d] for d in sample_counts}
print("Expect correct:", expect_correct)
total_expect_correct = round(sum(expect_correct.values()))
print("Total expect correct:", total_expect_correct)
percent_correct = round(100 * total_expect_correct / total_samples, 2)
print("Estimate that", total_expect_correct, "(=", percent_correct, "%) correct of the", total_samples, "that were assigned regimen 12 by Mykrobe, but phenotype assigned regimen 11.")
