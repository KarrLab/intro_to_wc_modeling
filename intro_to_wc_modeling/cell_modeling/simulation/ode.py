""" ODE simulation tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-06-23
:Copyright: 2017, Karr Lab
:License: MIT
"""

import matplotlib
# select a supported matplotlib backend if necessary
# matplotlib.use('Agg')
import matplotlib.pyplot
import numpy
import scipy.integrate
import os

def d_conc_d_t(concs, time):
    """ Calculate differentials for Goldbeter 1991 cell cycle model 
    (`BIOMD0000000003 <http://www.ebi.ac.uk/biomodels-main/BIOMD0000000003>`_)

    Args:
        time (obj:`float`): time
        concs (:obj:`numpy.ndarray`): array of current concentrations

    Returns:
        :obj:`numpy.ndarray`
    """
    cell = 1.0
    vi = 0.025
    kd = 0.01
    vd = 0.25
    Kd = 0.02
    K1 = 0.005
    V2 = 1.5
    K2 = 0.005
    K3 = 0.005
    V4 = 0.5
    K4 = 0.005
    VM1 = 3.
    VM3 = 1.
    Kc = 0.5

    C = concs[0] # cyclin
    M = concs[1] # cdc2
    X = concs[2] # cyclin protease

    V1 = C * VM1 / (C + Kc)
    V3 = M * VM3

    r_cyclin_creation = cell * vi
    r_default_cyclin_degradation = C * cell * kd
    r_cdc2_triggered_cyclin_degradation = C * cell * vd * X / (C + Kd)
    r_activation_of_cdc2 = cell * (1 - M) * V1 / (K1 - M + 1)
    r_deactivation_of_cdc2 = cell * M * V2 / (K2 + M)
    r_activation_of_cyclin_protease = cell * V3 * (1 - X) / (K3 - X + 1)
    r_deactivation_of_cyclin_protease = cell * V4 * X / (K4 + X)

    d_cyclin_dt = \
        + r_cyclin_creation \
        - r_default_cyclin_degradation \
        - r_cdc2_triggered_cyclin_degradation
    d_cdc2_dt = \
        + r_activation_of_cdc2 \
        - r_deactivation_of_cdc2
    d_cyclin_protease_dt = \
        + r_activation_of_cyclin_protease \
        - r_deactivation_of_cyclin_protease

    return numpy.array([
        d_cyclin_dt, 
        d_cdc2_dt,
        d_cyclin_protease_dt
        ])

# initial conditions
init_concs = numpy.array([0.01, 0.01, 0.01])

# integrate model
time_max = 100
time_step = 0.1
time_hist = numpy.linspace(0., time_max, time_max / time_step + 1)
conc_hist = scipy.integrate.odeint(d_conc_d_t, init_concs, time_hist)

# plot results
line_cyclin, = matplotlib.pyplot.plot(time_hist, conc_hist[:, 0], 'b-', label='Cyclin')
line_cdc2, = matplotlib.pyplot.plot(time_hist, conc_hist[:, 1], 'r-', label='Cdc2')
line_cyclin_protease, = matplotlib.pyplot.plot(time_hist, conc_hist[:, 2], 'g-', label='Protease')
matplotlib.pyplot.legend([line_cyclin, line_cdc2, line_cyclin_protease], ['Cyclin', 'Cdc2', 'Protease'])
matplotlib.pyplot.xlim(0, time_max)
matplotlib.pyplot.xlabel('Time (min)')
matplotlib.pyplot.ylabel('Cyclin concentration and fraction of\nactive Cdc2 and cyclin protease')
matplotlib.pyplot.gca().spines['top'].set_visible(False)
matplotlib.pyplot.gca().spines['right'].set_visible(False)

# display figure
# matplotlib.pyplot.show()

# save figure
filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'tutorials',
                        'cell_modeling', 'simulation', 'ode-results.png')
matplotlib.pyplot.savefig(filename, transparent=True, bbox_inches='tight')
matplotlib.pyplot.close()