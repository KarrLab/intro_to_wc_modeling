''' Test the wc_lang tutorial

:Author: Arthur Goldberg, Arthur.Goldberg@mssm.edu
:Date: 2017-06-13
:Copyright: 2017, Karr Lab
:License: MIT
'''

from intro_to_wc_modeling.wc_modeling.wc_lang_tutorial import core
import unittest


class TestWC_Lang(unittest.TestCase):

    def test(self):
        examples = []
        examples.append("read model")
        examples.append("write a model to a set of .tsv files")
        examples.append("read a model from a set of .tsv files")
        examples.append("referenced model attributes")
        examples.append("referenced model convenience methods")
        examples.append("get_reactions entry 0")
        examples.append("created model")
        examples.append("validate model")
        examples.append("normalize model")
        results = core.main()
        for example, result in zip(examples, results):
            self.assertIn(example, result)
