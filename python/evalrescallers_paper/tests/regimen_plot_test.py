from collections import OrderedDict
import os
import unittest

from evalrescallers_paper import regimen_plot

modules_dir = os.path.dirname(os.path.abspath(regimen_plot.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data', 'regimen_plot')


class TestRegimenPlot(unittest.TestCase):
    def test_make_regimen_plot(self):
        '''test make_regimen_plot'''
        infile = os.path.join(data_dir, 'make_regimen_plot.tsv')
        tmp_out = 'tmp.make_regimen_plot.svg'
        data = regimen_plot.load_regimen_counts_tsv(infile, {'dataset1'})
        regimen_plot.plot_one_tool(data['tool1'], tmp_out, ignore={(0,0)})
        assert os.path.exists(tmp_out)
        assert os.path.exists(tmp_out.replace('.svg', '.pdf'))
        os.unlink(tmp_out)
        os.unlink(tmp_out.replace('.svg', '.pdf'))

