""" Stochastic simulation tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-06-22
:Copyright: 2017, Karr Lab
:License: MIT
"""

from matplotlib import pyplot
import numpy
import os

# represent the reaction and rate laws of the model
# - first reaction: synthesis
# - second reaction: degradation

reaction_stochiometries = [1, -1]

k_syn = 2.5 # 1/s
k_deg = 0.5 # 1/s/molecule
def kinetic_laws(copy_number):
    return numpy.array([
        k_syn,
        k_deg * copy_number,
        ])

# initial copy number
init_copy_number = 10


def simulate(reaction_stochiometries, kinetic_laws, init_copy_number, time_max, time_step):
    """ Run a stochastic simulation

    Args:
       reaction_stochiometries (:obj:`list` of :obj:`int`): list of stoichiometries of the protein in each reaction
       kinetic_laws (:obj:`list` of :obj:`function`): list of kinetic law function
       init_copy_number (:obj:`int`): initial copy number
       time_max (:obj:`float`): simulation length
       time_step (:obj:`float`): frequency to record predicted dynamics

    Returns:
        :obj:`tuple`:

            * :obj:`numpy.ndarray`: time points
            * :obj:`numpy.ndarray`: predicted copy number at each time point
    """

    # data structure to store predicted copy numbers
    time_hist = numpy.linspace(0., time_max, int(time_max / time_step + 1))
    copy_number_hist = numpy.full(int(time_max / time_step + 1), numpy.nan)
    copy_number_hist[0] = init_copy_number

    # initial conditions
    time = 0
    copy_number = init_copy_number

    # iterate over time
    while time < time_max:
        # calculate reaction properties/rates
        propensities = kinetic_laws(copy_number)
        total_propensity = numpy.sum(propensities)

        # select the length of the time step from an exponential distributuon
        dt = numpy.random.exponential(1. / total_propensity)

        # select the next reaction to fire
        i_reaction = numpy.random.choice(len(propensities), p=propensities / total_propensity)

        # update the time and copy number based on the selected reaction
        time += dt
        copy_number += reaction_stochiometries[i_reaction]

        # store copy number history
        #print(time)
        if time < time_max:
            copy_number_hist[int(numpy.ceil(time / time_step)):] = copy_number

    return (time_hist, copy_number_hist)

def main():
    # seed random number generator
    numpy.random.seed(0)

    # run simulations
    time_max = 25.
    time_step = 1.
    n_simulations = 100
    copy_number_hist = numpy.full((int(time_max / time_step + 1), n_simulations), numpy.nan)
    for i_sim in range(n_simulations):
        time_hist, copy_number_hist[:, i_sim] = simulate(reaction_stochiometries, kinetic_laws, init_copy_number, time_max, time_step)

    # plot results
    for i_sim in range(n_simulations):
        color = (
            float(i_sim) / (float(n_simulations) - 1.) / 2,
            float(i_sim) / (float(n_simulations) - 1.) / 2,
            float(i_sim) / (float(n_simulations) - 1.) / 2,
        )
        pyplot.plot(time_hist, copy_number_hist[:, i_sim], linestyle='-', color=color, linewidth=0.5)

    pyplot.fill_between(time_hist,
        numpy.mean(copy_number_hist, 1) - numpy.std(copy_number_hist, 1),
        numpy.mean(copy_number_hist, 1) + numpy.std(copy_number_hist, 1),
        facecolor=(1, 0, 0, 0.5))
    pyplot.plot(time_hist, numpy.mean(copy_number_hist, 1), linestyle='-', color='r', linewidth=3)

    pyplot.xlim(0, time_max)
    pyplot.xlabel('Time (s)')
    pyplot.ylabel('Copy number')
    pyplot.gca().spines['top'].set_visible(False)
    pyplot.gca().spines['right'].set_visible(False)

    # display figure
    # pyplot.show()

    # save figure
    filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs',
                            'cell_modeling', 'simulation', 'stochastic-results.png')
    pyplot.savefig(filename, transparent=True, bbox_inches='tight')
    pyplot.close()