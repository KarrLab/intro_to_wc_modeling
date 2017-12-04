""" Tests the database tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-06-08
:Copyright: 2017, Karr Lab
:License: MIT
"""

from intro_to_wc_modeling.concepts_skills.software_engineering.databases import core
import unittest


class TestDatabaseTutorial(unittest.TestCase):

    def test(self):
        core.main()
