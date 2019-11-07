BootStrap: debootstrap
OSVersion: bionic
MirrorURL: http://us.archive.ubuntu.com/ubuntu/

%environment
    PATH=/evalrescallers_paper/scripts:$PATH

%setup
    rsync -a python scripts $SINGULARITY_ROOTFS/evalrescallers_paper


%post
    apt-get update
    apt-get install -y software-properties-common
    apt-add-repository universe
    apt-get update
    apt-get install -y python3-pip python3-dev python3-setuptools python3-mpltoolkits.basemap inkscape git r-base r-cran-ggplot2 texlive-latex-recommended texlive-latex-extra texlive-fonts-extra

    cd /
    git clone https://github.com/iqbal-lab-org/tb-amr-benchmarking
    cd tb-amr-benchmarking/python
    git checkout 93bd3927f9be2720064874c072d6d74fcea36d4e
    python3 setup.py install

    cd /evalrescallers_paper/python
    python3 setup.py test
    # python3 setup.py test does not include the data directory from this repo
    # when it installs, but pip3 does.
    pip3 install .

