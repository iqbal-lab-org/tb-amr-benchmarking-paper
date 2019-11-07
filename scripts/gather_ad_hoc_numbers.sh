#!/usr/bin/env bash
set -e


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && $3==2 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Check WHO figure 451 mono-isoniazid samples: $x"



x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && $3==2 && $4==1 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Mykrobe recommending a pan-susceptible TB regimen for mono-isoniazid resistant isolates: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 2 <= $3 && $3 <= 9 && $4==1 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 2-9, called regimen 1: $x"



x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 2 <= $3 && $3 <= 9 && $4==10 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 2-9, called regimen 10: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && 2 <= $3 && $3 <= 9 && 10 <= $4 && $4 <= 11 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 2-9, called regimen 10 or 11: $x"




x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && $3 == 10 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Check 2872 rifampicin resistant M. tuberculosis isolates for which first-line drugs phenotyping justified initiation of a MDR-TB treatment regimen: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && $3 == 10 && $4 <= 9 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 10, called falsely identified as being less resistant: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && $3 == 10 && $4 == 1 {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Truth regimen 10, called regimen is 1: $x"


x=$(awk '$1~/^10k/ && $2=="Mykrobe.201901" && $3 == 10 && $4 == 11   {s+=$NF} END{print s}' r_is_resistant.regimen_counts.summary.tsv)
echo "Third, a significant subset (798) is assigned to an XDR-TB regimen: $x"
