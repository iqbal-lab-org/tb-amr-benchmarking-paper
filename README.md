# tb-amr-benchmarking-paper

Code to generate publication figures and tables from output of
[tb-amr-benchmarking](https://github.com/iqbal-lab-org/tb-amr-benchmarking).

## Installation

Build the singularity container by running this
from the root of this repository:

    sudo singularity build benchmark.img Singularity


## Usage

A JSON file made by the
[tb-amr-benchmarking pipeline](https://github.com/iqbal-lab-org/tb-amr-benchmarking)
is required. Assuming it is called `summary.json`, generate the results and
figures by running:

    singularity exec benchmark.img evalrescallers_make_figs_and_tables summary.json OUT

which makes a new directory called `OUT/`. Various stats were needed for the
main text of the paper, which were calculated by running this:

    cd OUT
    singularity exec benchmark.img gather_ad_hoc_numbers.sh

