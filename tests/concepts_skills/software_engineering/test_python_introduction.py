""" Tests the python introduction exercises

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-07-11
:Copyright: 2017, Karr Lab
:License: MIT
"""

from intro_to_wc_modeling.concepts_skills.software_engineering import python_introduction
import unittest


class TestPythonIntroduction(unittest.TestCase):

    def test(self):
        python_introduction.main()
