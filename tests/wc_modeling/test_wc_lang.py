''' Test the wc_lang tutorial

:Author: Arthur Goldberg, Arthur.Goldberg@mssm.edu
:Date: 2017-06-13
:Copyright: 2017, Karr Lab
:License: MIT
'''

from intro_to_wc_modeling.wc_modeling.wc_lang_tutorial import core
import shutil
import tempfile
import unittest


class TestWC_Lang(unittest.TestCase):

    def setUp(self):
        self.dirname = tempfile.mkdtemp()
        shutil.rmtree(self.dirname)

    def tearDown(self):
        shutil.rmtree(self.dirname)

    def test(self):
        core.main(examples_dir=self.dirname)
