import glob
from setuptools import setup, find_packages


setup(
    name='evalrescallers_paper',
    version='0.0.2',
    description='Evaluation of TB AMR callers -- make figues and tables',
    packages = find_packages(),
    package_data={'evalrescallers_paper': ['data/*']},
    author='Martin Hunt',
    author_email='mhunt@ebi.ac.uk',
    url='https://github.com/iqbal-lab-org/tb-amr-benchmarking-paper',
    scripts=glob.glob('scripts/*'),
    test_suite='nose.collector',
    tests_require=['nose >= 1.3'],
    install_requires=[
        'evalrescallers'
    ],
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
    ],
)
