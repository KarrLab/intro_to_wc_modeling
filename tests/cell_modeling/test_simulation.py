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

    def test_mrna_and_proteins_using_several_methods(self):
        from intro_to_wc_modeling.cell_modeling.simulation import mrna_and_proteins_using_several_methods
        mrna_and_proteins_using_several_methods.deterministic_exercise()
        mrna_and_proteins_using_several_methods.probability_distribution_exercise()
        mrna_and_proteins_using_several_methods.trajectory_exercise()

    def test_multi_algorithm_simulation(self):
        from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import simulation
        simulation.main()

    def test_multi_algorithm_submodel_simulation(self):
        from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import submodel_simulation        
        submodel_simulation.main()
