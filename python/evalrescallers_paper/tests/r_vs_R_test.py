from collections import OrderedDict
import os
import unittest

from evalrescallers_paper import r_vs_R

modules_dir = os.path.dirname(os.path.abspath(r_vs_R.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data', 'r_vs_R')


class Test_r_vs_R(unittest.TestCase):
    def test_load_accuracy_stats_file(self):
        '''test load_accuracy_stats_file'''
        infile = os.path.join(data_dir, 'load_accuracy_stats_file.tsv')
        got = r_vs_R.load_accuracy_stats_file(infile, 'dataset1', 'tool1')
        expect = {
            'drug1': OrderedDict([('Dataset', 'dataset1'),
                       ('Tool', 'tool1'),
                       ('Drug', 'drug1'),
                       ('foo', 1),
                       ('bar', 2)]),
             'drug2': OrderedDict([('Dataset', 'dataset1'),
                       ('Tool', 'tool1'),
                       ('Drug', 'drug2'),
                       ('foo', 3),
                       ('bar', 4)])
        }
        self.assertEqual(expect, got)


    def test_get_data_for_differences_between_stats_files(self):
        '''test get_data_for_differences_between_stats_files'''
        # FIXME
        pass


    def test_report_diffs_between_stats_files(self):
        '''test report_diffs_between_stats_files'''
        # FIXME
        pass

