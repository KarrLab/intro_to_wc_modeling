""" Tests the model composition tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-08-30
:Copyright: 2017, Karr Lab
:License: MIT
"""

import shutil
import tempfile
import unittest


class TestModelCompositionTutorial(unittest.TestCase):

    def setUp(self):
        self.out_dir = tempfile.mkdtemp()
        shutil.rmtree(self.out_dir)

    def tearDown(self):
        shutil.rmtree(self.out_dir)

    def test(self):
        from intro_to_wc_modeling.cell_modeling import model_composition
        model_composition.main(out_dir=self.out_dir)
