from collections import OrderedDict
import filecmp
import json
import os
import shutil
import subprocess
import unittest

from evalrescallers_paper import latex

modules_dir = os.path.dirname(os.path.abspath(latex.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data', 'latex')


class TestLatex(unittest.TestCase):
    def test_tool_accuracy_table_on_one_dataset(self):
        '''test tool_accuracy_table_on_one_dataset'''
        infile = os.path.join(data_dir, 'tool_accuracy_table_on_one_dataset.tsv')
        outprefix = 'tmp.latex.tool_accuracy_table_on_one_dataset'
        table_file = f'{outprefix}.table.tex'
        texfile = f'{outprefix}.tex'
        drugs = OrderedDict([('drug1', 'd1'), ('drug2', 'd2')])
        latex.tool_accuracy_table_on_one_dataset(infile, 'tool1', drugs, 'set2', table_file)

        # check the table it made compiles. With an underfull hbox of course.
        # (table is too side for the default page/margins)
        texfile = 'tmp.latex.tool_accuracy_table_on_one_dataset.tex'
        with open(texfile, 'w') as f:
            print(r'''\documentclass{article}''', file=f)
            print(r'''\begin{document}''', file=f)
            print(r'''\input{''' + table_file + '}', file=f)
            print(r'''\end{document}''', file=f)

        completed_process = subprocess.run(f'pdflatex {texfile}', shell=True)
        self.assertEqual(0, completed_process.returncode)
        self.assertTrue(os.path.exists(texfile.replace('.tex', '.pdf')))
        os.unlink(texfile)
        os.unlink(table_file)
        os.unlink(f'{outprefix}.pdf')
        os.unlink(f'{outprefix}.aux')
        os.unlink(f'{outprefix}.log')


    def test_regimen_summary_table(self):
        '''test regimen_summary_table'''
        infile = os.path.join(data_dir, 'regimen_summary_table.tsv')
        outprefix = 'tmp.regimen_summary_table'
        table_file = f'{outprefix}.table.tex'
        texfile = f'{outprefix}.tex'
        datasets = {'10k_test', '10k_validate'}
        tools = {'ARIBA', 'KvarQ'}
        latex.regimen_summary_table(infile, table_file, datasets, tools)

        with open(texfile, 'w') as f:
            print(r'''\documentclass{article}''', file=f)
            print(r'''\begin{document}''', file=f)
            print(r'''\input{''' + table_file + '}', file=f)
            print(r'''\end{document}''', file=f)

        completed_process = subprocess.run(f'pdflatex {texfile}', shell=True)
        self.assertEqual(0, completed_process.returncode)
        self.assertTrue(os.path.exists(texfile.replace('.tex', '.pdf')))
        os.unlink(texfile)
        os.unlink(table_file)
        os.unlink(f'{outprefix}.pdf')
        os.unlink(f'{outprefix}.aux')
        os.unlink(f'{outprefix}.log')
