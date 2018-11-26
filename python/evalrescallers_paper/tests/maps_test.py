import os
import unittest

from evalrescallers_paper import maps

modules_dir = os.path.dirname(os.path.abspath(maps.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data', 'maps')

class TestMaps(unittest.TestCase):
    def test_make_maps(self):
        '''test make maps'''
        outprefix = 'tmp.make_maps'
        country_counts = {
            'Australia': {'test': 10, 'train': 20, 'validate': 0},
            'Belgium': {'test':5, 'train':100, 'validate':1000},
            'Germany': {'test':0, 'train':1, 'validate':20},
            'Italy': {'test':7, 'train':20, 'validate':0},
            'Netherlands': {'test':42, 'train':4242, 'validate':0},
            'Serbia': {'test':43, 'train':0, 'validate':0},
            'Spain': {'test':11, 'train':0, 'validate':9},
            'UK': {'test':12, 'train':6, 'validate':0},
        }

        maps.make_maps(outprefix, country_counts)
        files = [
            f'{outprefix}.europe.pdf',
            f'{outprefix}.world.pdf',
            f'{outprefix}.legend.pdf',
        ]
        for filename in files:
            self.assertTrue(os.path.exists(filename))
            os.unlink(filename)

