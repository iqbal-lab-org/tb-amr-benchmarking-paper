import filecmp
import json
import os
import unittest

from evalrescallers_paper import run_time_and_memory

modules_dir = os.path.dirname(os.path.abspath(run_time_and_memory.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data', 'run_time_and_memory')


class TestRunTimeAndMemory(unittest.TestCase):
    def test_json_to_tsv(self):
        '''test json_to_tsv'''
        json_in = os.path.join(data_dir, 'json_to_tsv.json')
        with open(json_in) as f:
            json_data = json.load(f)
        tsv_out = 'tmp.run_time_and_memory.json_to_tsv.tsv'
        run_time_and_memory.json_to_tsv(json_data, tsv_out)
        expected = os.path.join(data_dir, 'json_to_tsv.tsv')
        self.assertTrue(filecmp.cmp(expected, tsv_out, shallow=False))
        os.unlink(tsv_out)


    def test_tsv_to_plot(self):
        '''test tsv_to_plot'''
        tsv_in = os.path.join(data_dir, 'tsv_to_plot.tsv')
        outprefix = 'tmp.run_time_and_memory.tsv_to_plot'
        run_time_and_memory.tsv_to_plot(tsv_in, outprefix)
        self.assertTrue(os.path.exists(f'{outprefix}.time.pdf'))
        os.unlink(f'{outprefix}.time.pdf')
        self.assertTrue(os.path.exists(f'{outprefix}.memory.pdf'))
        os.unlink(f'{outprefix}.memory.pdf')
        os.unlink(f'{outprefix}.R')

