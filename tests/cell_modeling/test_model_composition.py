""" Tests the model composition tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-08-30
:Copyright: 2017, Karr Lab
:License: MIT
"""

import unittest


class TestModelCompositionTutorial(unittest.TestCase):

    def test(self):
        from intro_to_wc_modeling.cell_modeling import model_composition
        model_composition.exercise_merge_mathematically_like_models()
