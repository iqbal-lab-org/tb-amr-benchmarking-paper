BootStrap: debootstrap
OSVersion: bionic
MirrorURL: http://us.archive.ubuntu.com/ubuntu/

%setup
    rsync -a python $SINGULARITY_ROOTFS/evalrescallers_paper


%post
    apt-get update
    apt-get install -y software-properties-common
    apt-add-repository universe
    apt-get update
    apt-get install -y python3-dev python3-setuptools python3-mpltoolkits.basemap inkscape git r-base r-cran-ggplot2

    cd /
    git clone https://github.com/iqbal-lab-org/tb-amr-benchmarking
    cd tb-amr-benchmarking/python
    git checkout 27bc4fed12408dbec794a5bd8a0421718b1886fa
    python3 setup.py install

    cd /evalrescallers_paper/python
    python3 setup.py test
    python3 setup.py install

