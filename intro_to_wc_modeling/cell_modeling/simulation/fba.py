""" FBA simulation tutorial

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-06-22
:Copyright: 2017, Karr Lab
:License: MIT
"""

import matplotlib.pyplot
import numpy
import optlang
import os

# create a model
model = optlang.Model()

# add a variable for each reaction flux
glc_tx = optlang.Variable('glc_tx', lb=0)
aa_tx = optlang.Variable('aa_tx', lb=0)
ntp_synth = optlang.Variable('ntp_synth', lb=0)

# add a variable for the growth reaction
growth = optlang.Variable('growth', lb=0)

# add variaable for each exchange reaction
glc_ex = optlang.Variable('glc_ex', lb=0)
aa_ex = optlang.Variable('aa_ex', lb=0)
biomass_ex = optlang.Variable('biomass_ex', lb=0)

# add a constraint for the rate of change of each species
glc_e = optlang.Constraint(glc_ex - glc_tx, lb=0, ub=0)
glc_c = optlang.Constraint(glc_tx - ntp_synth - growth, lb=0, ub=0)
aa_e = optlang.Constraint(aa_ex - aa_tx, lb=0, ub=0)
aa_c = optlang.Constraint(aa_tx - growth, lb=0, ub=0)
ntp_c = optlang.Constraint(ntp_synth - growth, lb=0, ub=0)
biomass = optlang.Constraint(growth - biomass_ex, lb=0, ub=0)

model.add([glc_e, glc_c, aa_e, aa_c, ntp_c, biomass])

# Set the objective to maximize growth
model.objective = optlang.Objective(growth, direction='max')

# set the initial conditions
init_conc_glc_e = 200.
init_conc_aa_e = 120.
init_conc_biomass = 1.

# setup history to store time
time_max = 70
time_hist = numpy.array(range(time_max + 1))
flux_hist = numpy.full((time_max + 1, len(model.variables)), numpy.nan)
growth_hist = numpy.full(time_max + 1, numpy.nan)
conc_hist = numpy.full((time_max + 1, 3), numpy.nan)

# iterate over time
variable_names = model.variables.keys()
conc_glc_e = init_conc_glc_e
conc_aa_e = init_conc_aa_e
conc_biomass = init_conc_biomass
for i_time in range(time_max + 1):
    # constrain fluxes based on avialable nutrients
    glc_tx.ub = 5e-3 * conc_glc_e * conc_biomass
    aa_tx.ub = 1e-3 * conc_aa_e * conc_biomass

    # solve for the maximum growth and optimal fluxes
    status = model.optimize()
    assert(status == 'optimal')

    # store history
    growth_hist[i_time] = model.objective.value
    for i_var, var_name in enumerate(variable_names):
        flux_hist[i_time, i_var] = model.variables[var_name].primal

    conc_hist[i_time, 0] = conc_glc_e
    conc_hist[i_time, 1] = conc_aa_e
    conc_hist[i_time, 2] = conc_biomass

    # update concentrations
    conc_glc_e -= model.variables['glc_tx'].primal
    conc_aa_e -= model.variables['aa_tx'].primal
    conc_biomass += model.variables['growth'].primal

    conc_glc_e = max(0, conc_glc_e)
    conc_aa_e = max(0, conc_aa_e)
    conc_biomass = max(0, conc_biomass)

# plot results
matplotlib.use('Agg')

line_glc, = matplotlib.pyplot.plot(time_hist, conc_hist[:, 0], 'r-', label='Glucose')
line_aa, = matplotlib.pyplot.plot(time_hist, conc_hist[:, 1], 'g-', label='Amino acid')
line_biomass, = matplotlib.pyplot.plot(time_hist, conc_hist[:, 2], 'b-', label='Biomass')
matplotlib.pyplot.legend([line_glc, line_aa, line_biomass], ['Glucose', 'Amino acid', 'Biomass'])
matplotlib.pyplot.xlim(0, time_max)
matplotlib.pyplot.xlabel('Time')
matplotlib.pyplot.ylabel('Concentration')
matplotlib.pyplot.gca().spines['top'].set_visible(False)
matplotlib.pyplot.gca().spines['right'].set_visible(False)

# display figure
# matplotlib.pyplot.show()

# save figure
filename = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'docs', 'tutorials',
                        'cell_modeling', 'simulation', 'fba-results.png')
matplotlib.pyplot.savefig(filename, transparent=True, bbox_inches='tight')
matplotlib.pyplot.close()
