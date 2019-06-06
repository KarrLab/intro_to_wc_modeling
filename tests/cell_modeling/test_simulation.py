""" Tests the simulation tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-06-22
:Copyright: 2017, Karr Lab
:License: MIT
"""

from intro_to_wc_modeling.cell_modeling.simulation import mrna_and_proteins_using_several_methods
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import analysis
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import model
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import submodel_simulation
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import simulation
import intro_to_wc_modeling.cell_modeling.simulation.boolean
import intro_to_wc_modeling.cell_modeling.simulation.dfba
import intro_to_wc_modeling.cell_modeling.simulation.ode
import intro_to_wc_modeling.cell_modeling.simulation.stochastic
import numpy
import shutil
import tempfile
import unittest


class TestSimulationTutorial(unittest.TestCase):

    def test_boolean_exercise(self):
        intro_to_wc_modeling.cell_modeling.simulation.boolean.main()

    def test_ode_exercise(self):
        intro_to_wc_modeling.cell_modeling.simulation.ode.main()

    def test_stochastic_exercise(self):
        intro_to_wc_modeling.cell_modeling.simulation.stochastic.main()

    def test_dfba_exercise(self):
        intro_to_wc_modeling.cell_modeling.simulation.dfba.main()

    def test_dfba_exercise_negative_concentration(self):
        init_concs = {
            'glc_e': 200.,
            'aa_e': 120.,
            'biomass': 1e8,
        }
        with self.assertRaisesRegex(Exception, 'below 0'):
            intro_to_wc_modeling.cell_modeling.simulation.dfba.main(init_concs=init_concs)

    def test_mrna_and_proteins_using_several_methods_deterministic_exercise(self):
        mrna_and_proteins_using_several_methods.deterministic_exercise()

    def test_mrna_and_proteins_using_several_methods_probability_distribution_exercise(self):
        mrna_and_proteins_using_several_methods.probability_distribution_exercise()

    def test_mrna_and_proteins_using_several_methods_trajectory_exercise(self):
        mrna_and_proteins_using_several_methods.trajectory_exercise()

    def test_get_steady_state(self):
        sim = mrna_and_proteins_using_several_methods.OdeSimulation()
        self.assertEqual(sim.get_steady_stability(sim.jacobian(None)), 'stable sink')

        sim = mrna_and_proteins_using_several_methods.OdeSimulation()
        sim.k_n = 1
        sim.gamma_m = -1
        sim.gamma_n = -1
        self.assertEqual(sim.get_steady_stability(sim.jacobian(None)), 'unstable source')

        sim = mrna_and_proteins_using_several_methods.OdeSimulation()
        sim.k_n = 1
        sim.gamma_m = 0
        sim.gamma_n = 0
        self.assertEqual(sim.get_steady_stability(sim.jacobian(None)), 'unstable saddle')

        sim = mrna_and_proteins_using_several_methods.OdeSimulation()
        self.assertEqual(sim.get_steady_stability(numpy.array([[-1, -1], [1, -1]])), 'stable spiral sink')

        sim = mrna_and_proteins_using_several_methods.OdeSimulation()
        self.assertEqual(sim.get_steady_stability(numpy.array([[1, 1], [-1, 1]])), 'unstable spiral source')


class TestMultiAlgorithm(unittest.TestCase):

    def test_simulation(self):
        # make temporary directory
        dirname = tempfile.mkdtemp()
        shutil.rmtree(dirname)

        # simulate and plot results
        mdl, time, volume, growth, speciesCounts = simulation.main(output_directory=dirname)

        # Check if simulation implemented correctly
        self.assertGreater(volume[-1], 1.9 * volume[0])
        self.assertLess(volume[-1], 2.1 * volume[0])

        # cleanup
        shutil.rmtree(dirname)

    def test_submodel_simulation(self):
        # make temporary directory
        dirname = tempfile.mkdtemp()
        shutil.rmtree(dirname)

        # simulate and plot results
        mdl, time, volume, growth, speciesCounts = submodel_simulation.main(output_directory=dirname)

        # test
        self.assertGreater(growth[-1], 1.9 * growth[0])
        self.assertLess(growth[-1], 2.1 * growth[0])

        totalProt = numpy.zeros(len(time))
        for species in mdl.getComponentById('Metabolism').species:
            if species.species.type == 'Protein':
                totalProt += speciesCounts[species.id]
        self.assertGreater(totalProt[-1], 1.9 * totalProt[0])
        self.assertLess(totalProt[-1], 2.1 * totalProt[0])

        # cleanup
        shutil.rmtree(dirname)

    def test_analysis(self):
        # get y data
        with self.assertRaisesRegex(Exception, 'Invalid model type'):
            analysis.get_y_data(None, None, 'a[b]')

        # unit scaling
        scale_um = analysis.get_scale('uM', 'c', 1., 1.)
        scale_mm = analysis.get_scale('mM', 'e', 1., 1.)
        self.assertAlmostEqual(scale_mm, scale_um * 1e3, places=7)

        with self.assertRaisesRegex(Exception, 'Invalid units'):
            analysis.get_scale('', 'c', 1., 1.)

    def test_containsCarbon(self):
        self.assertTrue(model.Species(empiricalFormula='C').containsCarbon())
        self.assertFalse(model.Species(empiricalFormula='H').containsCarbon())

    def test_parseStoichiometry_exception(self):
        with self.assertRaisesRegex(ValueError, 'Invalid stoichiometry:'):
            model.parseStoichiometry('[]: ')
