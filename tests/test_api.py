""" Tests API

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2018-03-12
:Copyright: 2018, Karr Lab
:License: MIT
"""

import intro_to_wc_modeling
import types
import unittest


class ApiTestCase(unittest.TestCase):
    def test(self):
        self.assertIsInstance(intro_to_wc_modeling, types.ModuleType)

        self.assertIsInstance(intro_to_wc_modeling.cell_modeling, types.ModuleType)
        self.assertIsInstance(intro_to_wc_modeling.cell_modeling.model_composition, types.ModuleType)
        self.assertIsInstance(intro_to_wc_modeling.cell_modeling.simulation, types.ModuleType)
        self.assertIsInstance(intro_to_wc_modeling.cell_modeling.simulation.boolean, types.ModuleType)
        self.assertIsInstance(intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm, types.ModuleType)
        self.assertIsInstance(intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm.analysis, types.ModuleType)

        self.assertIsInstance(intro_to_wc_modeling.concepts_skills, types.ModuleType)
        self.assertIsInstance(intro_to_wc_modeling.concepts_skills.software_engineering, types.ModuleType)
        self.assertIsInstance(intro_to_wc_modeling.concepts_skills.software_engineering.databases, types.ModuleType)
        self.assertIsInstance(intro_to_wc_modeling.concepts_skills.software_engineering.databases.main, types.FunctionType)
        self.assertIsInstance(intro_to_wc_modeling.concepts_skills.software_engineering.matplotlib_example, types.ModuleType)
        self.assertIsInstance(intro_to_wc_modeling.concepts_skills.software_engineering.unit_testing, types.ModuleType)
        self.assertIsInstance(intro_to_wc_modeling.concepts_skills.software_engineering.unit_testing.Simulation, type)

        self.assertIsInstance(intro_to_wc_modeling.wc_modeling, types.ModuleType)
        self.assertIsInstance(intro_to_wc_modeling.wc_modeling.wc_lang_tutorial, types.ModuleType)
        self.assertIsInstance(intro_to_wc_modeling.wc_modeling.wc_lang_tutorial.main, types.FunctionType)
