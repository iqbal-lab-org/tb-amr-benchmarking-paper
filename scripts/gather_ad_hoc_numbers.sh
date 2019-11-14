#!/usr/bin/env bash
set -e


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && $3==2 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Check WHO figure 451 mono-isoniazid samples: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && $3==2 && $5==1 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Mykrobe recommending a pan-susceptible TB regimen for mono-isoniazid resistant isolates: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 2 <= $3 && $3 <= 9 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Total where truth regimen is 2-9: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 2 <= $3 && $3 <= 9 && $5==1 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 2-9, called regimen 1: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 2 <= $3 && $3 <= 9 && $5==10 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 2-9, called regimen 10: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 2 <= $3 && $3 <= 9 && 10 <= $5 && $5 <= 11 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 2-9, called regimen 10 or 11: $x"

x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 2 <= $3 && $3 <= 9 && $5==11 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 2-9, called regimen 11: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 2 <= $3 && $3 <= 9 && $5==12 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 2-9, called regimen 12: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 3 <= $3 && $3 <= 9 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Total where truth regimen is 3-9: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 3 <= $3 && $3 <= 9 && $5==1 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 3-9, called regimen 1: $x"

x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 3 <= $3 && $3 <= 9 && $5==2 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 3-9, called regimen 2: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 3 <= $3 && $3 <= 9 && $5==10 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 3-9, called regimen 10: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 3 <= $3 && $3 <= 9 && $5==11 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 3-9, called regimen 11: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 3 <= $3 && $3 <= 9 && $5==12 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 3-9, called regimen 12: $x"

x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 10 <= $3 && $3 <= 12 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Total where truth regimen is 10-12: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && $3==11 && 1 <= $5 && $5 <= 9 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 11, called 1-9: $x"


echo "Truth regimen counts:"
awk '$1~/10k/ && $2=="Mykrobe.201901" {a[$3] += $NF} END{for (x in a) {print x"\t"a[x]}}' r_is_resistant.regimen_counts.summary.tsv | sort -n


echo
echo "Truth regimen 10 breakdown"
awk '$1~/10k/ && $2=="Mykrobe.201901" && $3==10' r_is_resistant.regimen_counts.summary.tsv | sort -k5n


echo
echo "Truth regimen 11 breakdown"
awk '$1~/10k/ && $2=="Mykrobe.201901" && $3==11' r_is_resistant.regimen_counts.summary.tsv | sort -k5n


