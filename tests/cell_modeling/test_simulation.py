""" Tests the simulation tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-06-22
:Copyright: 2017, Karr Lab
:License: MIT
"""

import unittest


class TestSimulationTutorial(unittest.TestCase):

    def test_boolean_exercise(self):
        import intro_to_wc_modeling.cell_modeling.simulation.boolean

    def test_ode_exercise(self):
        import intro_to_wc_modeling.cell_modeling.simulation.ode

    def test_stochastic_exercise(self):
        import intro_to_wc_modeling.cell_modeling.simulation.stochastic

    def test_fba_exercise(self):
        import intro_to_wc_modeling.cell_modeling.simulation.fba

    def test_stochastic_exercises(self):
        from intro_to_wc_modeling.cell_modeling.simulation import stochastic_exercises
        stochastic_exercises.deterministic_exercise()
        stochastic_exercises.probability_distribution_exercise()
        stochastic_exercises.trajectory_exercise()

    def test_multi_algorithm_simulation(self):
        from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import simulation
        simulation.main()

    def test_multi_algorithm_submodel_simulation(self):
        from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import submodel_simulation        
        submodel_simulation.main()
