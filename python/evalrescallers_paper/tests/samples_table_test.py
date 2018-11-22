import filecmp
import os
import unittest

from evalrescallers_paper import samples_table

modules_dir = os.path.dirname(os.path.abspath(samples_table.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data', 'samples_table')


class TestSamplesTable(unittest.TestCase):
    def test_make_samples_tsv(self):
        '''test make_samples_tsv'''
        # All that matters in the json_data is the keys. Is only
        # used to ask: is sample in json_data? So for testing, can
        # just use a set of IDs. Pick a few at random across the data.
        json_data = {
            'ERR038266',  # from ncomms10063-s7.txt
            'SRR2100931', # from ncomms10063-s8.txt
            'ERS457325',  # from ncomms10063-s9.txt
            'ERR553349',  # from ncomms10063-s10.txt
            'ERR067620',  # from 10k validate dataset
            'ERR2514066', # from 10k test dataset
        }
        outfile = 'tmp.samples_table.make_samples_tsv.tsv'
        samples_table.make_samples_tsv(json_data, outfile)
        expected = os.path.join(data_dir, 'make_samples_tsv.tsv')
        self.assertTrue(filecmp.cmp(expected, outfile, shallow=False))
        os.unlink(outfile)
