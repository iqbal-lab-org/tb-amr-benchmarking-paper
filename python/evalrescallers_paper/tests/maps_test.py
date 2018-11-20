import os
import unittest

from evalrescallers_paper import maps

modules_dir = os.path.dirname(os.path.abspath(maps.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data', 'maps')

class TestMaps(unittest.TestCase):
    def test_make_maps(self):
        '''test make maps'''
        outprefix = 'tmp.make_maps'
        maps.make_maps(outprefix)
        files = [
            f'{outprefix}.europe.pdf',
            f'{outprefix}.world.pdf',
            f'{outprefix}.legend.pdf',
        ]
        for filename in files:
            self.assertTrue(os.path.exists(filename))
            os.unlink(filename)

