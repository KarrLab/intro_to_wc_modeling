""" dFBA simulation tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Author: Arthur Goldberg, Arthur.Goldberg@mssm.edu
:Date: 2017-06-22
:Copyright: 2017, Karr Lab
:License: MIT
"""

from matplotlib import pyplot
import numpy
import optlang
import os


def main(init_concs=None):
    """ Run dFBA simsulation, plot results, and save plots

    Args:
        init_concs (:obj:`dict`, optional): initial concentrations
    """

    # create a model
    model = optlang.Model()

    # add variables for some reaction fluxes
    # 0 <= flux for all reactions, as indicated by lb=0
    glc_tx = optlang.Variable('glc_tx', lb=0)
    aa_tx = optlang.Variable('aa_tx', lb=0)
    ntp_synth = optlang.Variable('ntp_synth', lb=0)

    # add a variable for the growth reaction flux
    growth = optlang.Variable('growth', lb=0)

    # add a variable for each exchange reaction flux
    glc_ex = optlang.Variable('glc_ex', lb=0)
    aa_ex = optlang.Variable('aa_ex', lb=0)
    biomass_ex = optlang.Variable('biomass_ex', lb=0)

    # Since FBA assumes that all species are in steady state, constrain the rate of change of each species to 0.
    # We express the constraint as the difference between reaction(s) that produce the specie and
    # those that consume it, i.e., its net change. Setting lb=0 & ub=0 constrains the first argument to 0
    glc_e = optlang.Constraint(glc_ex - glc_tx, lb=0, ub=0)
    glc_c = optlang.Constraint(glc_tx - ntp_synth - growth, lb=0, ub=0)
    aa_e = optlang.Constraint(aa_ex - aa_tx, lb=0, ub=0)
    aa_c = optlang.Constraint(aa_tx - growth, lb=0, ub=0)
    ntp_c = optlang.Constraint(ntp_synth - growth, lb=0, ub=0)
    biomass = optlang.Constraint(growth - biomass_ex, lb=0, ub=0)

    # add all Constraints to the model
    model.add([glc_e, glc_c, aa_e, aa_c, ntp_c, biomass])

    # Set the objective to maximize growth
    model.objective = optlang.Objective(growth, direction='max')

    # observe these concentration variables
    observables = ['glc_e', 'aa_e', 'biomass']

    # set non-zero initial conditions
    if not init_concs:
        init_concs = dict(zip(observables, [200., 120., 1.]))

    # simulation end time
    time_max = 70

    # setup matrices to store the history of simulation predictions
    time_hist = numpy.array(range(time_max + 1))
    flux_hist = numpy.full((time_max + 1, len(model.variables)), numpy.nan)
    growth_hist = numpy.full(time_max + 1, numpy.nan)

    conc_hist = {}
    for observable in observables:
        conc_hist[observable] = numpy.full(time_max + 1, numpy.nan)

    # set initial concentrations
    concentrations = init_concs.copy()

    variable_names = model.variables.keys()

    # iterate over time
    for i_time in range(time_max + 1):

        # constrain fluxes based on avialable nutrients
        # todo: explain these expressions
        glc_ex.ub = 5e-3 * concentrations['glc_e'] * concentrations['biomass']
        aa_ex.ub = 1e-3 * concentrations['aa_e'] * concentrations['biomass']

        # solve for the maximum growth and optimal fluxes
        status = model.optimize()
        assert(status == 'optimal')

        # store history
        growth_hist[i_time] = model.objective.value
        for i_var, var_name in enumerate(variable_names):
            flux_hist[i_time, i_var] = model.variables[var_name].primal

        for observable in observables:
            conc_hist[observable][i_time] = concentrations[observable]

        # Update the concentrations which are being recorded.
        # Since the time step is 1, the concentration change = flux * 1
        concentrations['glc_e'] -= model.variables['glc_tx'].primal
        concentrations['aa_e'] -= model.variables['aa_tx'].primal
        concentrations['biomass'] += model.variables['growth'].primal

        for observable in observables:
            if concentrations[observable] < 0:
                raise ValueError("Error: concentration of {} at {}, which is below 0, at time {}".format(
                    observable, concentrations[observable], i_time))

    # plot results
    plot_labels = ['Glucose', 'Amino acid', 'Biomass']
    lines = []
    for observable, plot_label in zip(observables, plot_labels):
        lines.append(pyplot.plot(time_hist, conc_hist[observable], '-', label=plot_label)[0])
    pyplot.legend(lines, plot_labels)
    pyplot.xlim(0, time_max)
    pyplot.xlabel('Time (s)')
    pyplot.ylabel('Concentration')
    pyplot.gca().spines['top'].set_visible(False)
    pyplot.gca().spines['right'].set_visible(False)

    # display figure
    # pyplot.show()

    # save figure
    filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs',
                            'cell_modeling', 'simulation', 'dfba-results.png')
    pyplot.savefig(filename, transparent=True, bbox_inches='tight')
    pyplot.close()
