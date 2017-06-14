Mathematical representations and simulation algorithms
======================================================

There is wide range of mathematical representations that can be used model cells, ranging from coarse-grained representations such as Boolean networks to fine-grained representations such as spatial stochastic models. Below are several considerations for choosing a mathematical representation for a model.

* What are the relevant physical scales of the biology? Deterministic models are valid approximations when the fluctuations are small which often occurs when the flux scale is large. Conversely, stochastic models should be used when the fluctuations are large and/or they critically impact behavior.
* How much information is known about the biology? If significant information is known, then fine-grained models are possible. Conversely, if the biology is not well-characterized a fine-grained representation may be infeasible and a coarse-grained representation should be used.
* How much computational cost is acceptable? If you need a model to execute quickly or you anticipate running large numbers of simulations, it may be best to use a coarse-grained representation. Alternatively, if you want to build the most detailed model possible, you should use a fine-grained representation.
* What simulation software tools are available? Several tools are available to simulate single-algorithm models. However, there are few tools for simulating hybrid models. If you don't want to spend a lot of energy writing numerical simulation code, we recommend you focus on well-established mathematical representations.

The goal of this tutorial is to introduce you to the most commonly used mathematical representations for cell modeling, how they can be numerically simulated, how to fully specific a simulation, and several of the most commonly used simulation software programs.


Boolean/logical models
^^^^^^^^^^^^^^^^^^^^^^
Boolean models are composed of composed Boolean variables and logical functions which describe how the value of each variable is influenced by other variables. Logical or multi-level models are a generalization of Boolean models in which the variables can have two or more possible values. Importantly, Boolean models have no quantitative parameters or explicit timescales. Similarly, logical models have few quantitative parameters. Consequently, Boolean and logical models are often used to describe biological systems that have not yet been quantitatively characterized, as well as to build large models that contain many more variables/species and functions/interactions than could be calibrated in a more quantitative model.

Boolean models are simulated via timestep algorithms which divide the simulation into many small timesteps during which the simulator excecutes one of several `update schemes` that evaluate the logical functions and updates the Boolean variables. Below is a list of the most commonly used Boolean update schemes

* Synchronous updating: during each timestep, all of the functions are evaluated with the same node states and all of the nodes are updated with the results of the functions
* Asynchronous updating: during each timestep, only one or a subset of the logical functions are evaluated and only the corresponding subset of nodes are updated

    * Deterministic asynchronous updating: the timesteps iterate over the functions/rules in a deterministic order
    * Random asynchronous updating: at each timestep, the simulator randomly chooses one or more functions/nodes to update


Flux balance analysis (FBA)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Flux balance analysis (FBA) is a popular approach to simulating metabolism. Like ODE models, FBA is based on microscopic analyses of how the concentration of each species in the cell changes over time in response to the concentrations of other species. However, FBA leverages two additional sets of data and two additional assumptions. First, FBA incorporates estimates of the minimum and maximum possible flux of each reaction which, for a subset of reactions, can be obtained from experimental observations. Second, FBA incorporates an additional reaction which represents the assembly of metabolites into a cell and can be calibrated based on the observed cellular composition. Third, FBA assumes that the each species is at steady-state (:math:`\frac{dx}{dt} = 0`). This assumptions greatly constrains the model, thereby reducing the amount of data needed to build the model. However, this assumption also prevents FBA from making predictions about the dynamics of metabolic networks. Fourth, FBA assumes that cells have evolved to grow maximally fast. Together, these additional data and assumptions pose cell simulation as a linear optimization problem which can be solved using linear programming.

.. math::

    \text{Maximize}~ v_\text{growth} &= f' v \\
    \text{Subject to}~\\
    S v &= 0 \\
    v^\text{min} &\leq v \leq v^\text{max}, \\

where :math:`S_{ij}` is the stochiometry of species :math:`i` in reaction :math:`j`, :math:`v_j` is the flux of reaction :math:`j`, :math:`v^\text{min}_{j}` and :math:`v^\text{max}_j` are the upper and lower bounds of the flux of reaction :math:`j`, and :math:`f_\mu` is 1 for the biomass composition and 0 otherwise.


Ordinary differential equations (ODEs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Ordinary differential equations (ODEs) is one of the most commonly used approaches for modeling dynamical systems. ODE models are based on microscopic analyses of how the concentration of each species in the cell changes over time in response to the concentrations of other species. Because ODE assume that cells are well-mixed and that they behave deterministically, ODE models are most appropriate for small systems that involve large concentrations and high fluxes. ODE models can be simulated by numerically integrating the differential equations.  


Stochastic simulation
^^^^^^^^^^^^^^^^^^^^^
Like ODE models, stochastic models are based on microscopic analyses of how the concentration of each species in the cell changes over time in response to the concentrations of other species. However, stochastic simulation algorithms relax the assumption that cells behave deterministically. Instead, stochastic simulation algorithms assume that the rate of each reaction is Poisson-distributed. As a result, stochastic simulation algorithms generate sequences of reaction events at which the state of the cell discretely changes.

Because stochastic simulations are random, stochastic models should generally be simulated multiple times to sample the distribution of predicted cell behaviors. In general, these simulations should be run both using different random number generator seeds and different random initial conditions.

Stochastic simulation should be used to model systems that are sensitive to small fluctuations such as systems that involve small concentrations and small fluxes. However, stochastic simulation can be computationally expensive for large numbers due to the needs to resolve the exact order of every reaction and the need to run multiple simulations to sample the distribution of predicted cell behaviors.

Below is pseudo-code for the simplest stochastic simulation algorithm which is also known as the Gillespie algorithm::
    
    import numpy

    # represent the reaction and rate laws of the model
    reaction_stochiometries = numpy.array([ ... ])
    kinetic_laws = [...]

    # initialize the time and cell state
    time = 0
    copy_numbers = numpy.array([ ... ])
    
    while time < time_max:
        # calculate reaction properties/rates
        propensities = [kinetic_law(copy_numbers) for kinetic_law in kinetic_laws]
        total_propensity = sum(propensities)

        # select the length of the time step from an exponential distributuon
        dt = numpy.random.exponential(1 / total_propensity)

        # select the next reaction to fire
        i_reaction = numpy.random.choice(len(propensitites), p=propensitites / total_propensity)

        # update the time and cell state based on the selected reaction
        time += dt
        copy_numbers += reaction_stochiometries[:, i_reaction]

In addition to the above algorithm, there are many algorithms which approximate the results of the above algorithm with significantly lower computational costs. The most commonly used algorithm of these approximate simulation algorithms is the tau leaping algorithm.


Network-free simulation
^^^^^^^^^^^^^^^^^^^^^^^
Network-free simulation is a variant of stochastic simulation for simulating rule-based models in which the occupied species and active reactions are discovered dynamically during simulation rather than statistically enumerating all possible species and reactions prior to simulation. Network-free simulation is a mathematically equivalent algorithm for stochastic simulation. The key advantage of network-free simulation is that it can simulate models with very large or infinitely large state state spaces that cannot be simulated with conventional simulation algorithms. 


Multi-algorithmic simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To efficiently simulate entire cells, we must represent each aspect of a cell using the most appropriate mathematics and concurrently integrate or co-simulate the combined hybrid or multi-algorithmic model. For example, we must represent transcription as a stochastic model and represent metabolism as an FBA model. Hybrid simulation is an open area of research. Below is a summarize of several increasingly sophisticated hybrid simulation algorithms.

* Serial simulation: Divide the simulation into multiple small time steps. Within each time step, iteratively simulate the submodel and update the cell state. Optionally, simulate the models in a random order at each time step. This is a simple algorithm to implement. However, this algorithm violates the arrow of time by integrating submodels based on different states within each time step.
* Partitioning and merging: Divide the simulation into multiple small time steps. With each time step, partition the pool of each species into separate pools for each submodel. Simulate the submodels independently using the independent pools. Update the global species pools by merging the submodel pools. Species can be partitioned uniformly, based on their utilization during the previous time point, or based on a preliminary integration of the submodels. This is a relatively simple algorithm to implement for models whose state only represents concentrations and/or species copy number. However, it can be challenging to partition and merge rule-based models whose states are represented by graphs.
* Interpolation: For models that are composed of one discrete and one continuous model, we can append the continuous model to the discrete model as a single pseudo reaction, fire the reaction immediately after each discrete reaction, and periodically calculate the coefficients of the pseudo reaction by numerically integrating the continuous model. Furthermore, we could adaptive choose the frequency at which the continuous model is simulated based on the sensitivity of its predictions to its inputs from the discrete model. Overall, we believe this algorithm provides a good balance of accuracy and speed.
* Scheduling: Build a higher-order stochastic model which contains one pseudo-reaction per submodel. Set the propensity of each pseudo-reaction to the total propensity of the submodel. Use the Gillespie method to schedule the firing of the pseudo-reactions/submodels. This is the strategy used by E-Cell (Takahashi et al., 2004).
* Upscaling: For models that are composed of one discrete and one continuous model, we can append all of the continuous reactions model to the discrete model; periodically set their propensities by evaluating their kinetic laws, or in the case of FBA, calculating the optimal flux distribution; and select and fire the continuous reactions using the same mechanism as the discrete reactions. This algorithm is compelling, but is computationally expensive due to the need to resolve the order of every reaction including every continuous reaction.


Simulating individual submodels
-------------------------------
For calibration and testing, it is useful to simulate individual submodels of a larger model. To meaningfully simulate a submodel, you must `mock` the impact of all of the other submodels that the submodel interacts with. This can be done by creating coarse-grained versions of all of the other submodels which mimic their external behavior at a lower computational cost.


Simulation descriptions
-----------------------
To simulate a model, we must specify every aspect of the simulation including 

* The model that we want to simulate
* Any modifications of the model that we wish to simulate (e.g. modified parameter values)
* The initial conditions of the simulation
* The desired simulation algorithm
* The parameters of the simulation algorithm such as the initial seed and state of the random number generator

The `Simulation Experiment Description Markup Language <http://sed-ml.org>`_ (SED-ML) is one of the most commonly used languages for describing simulations. SED-ML is primarily designed to describe simulations of XML-based models such as models encoded in CellML and SBML. However, SED-ML can be used to describe the simulation of any model. `Simulation Experiment Specification via a Scala Layer <http://sessl.org>`_ (SESSL) is competing langauge simulation description language. 


Software tools
--------------

* `CellNOpt <http://www.cellnopt.org/>`_: Boolean simulator
* `Cell Collective <https://cellcollective.org>`_: online Boolean simulator
* `COPASI <http://copasi.org>`_: ODE and stochastic simulator
* `ECell <http://www.e-cell.org>`_: multi-algorithmic simulator
* `JWS Online <http://jjj.biochem.sun.ac.za/>`_: online ODE and stochastic simulator
* `libRoadRunner <http://libroadrunner.org/>`_: ODE and stochastic simulation library
* `NFSim <http://michaelsneddon.net/nfsim/>`_: stochastic network-free simulator
* `VCell <http://vcell.org/>`_: ODE, stochastic, and spatial simulator


Exercises
---------

* Write a synchronous Boolean simulator
* Write a Runge-kutta 4th order ODE integrator
* Write a Gillespie algorithm simulator
* Write a hybrid FBA/SSA simulator
* Use BioNetGen and/or NFSim to simulate a model describe using BNGL rules
* Build a composite model and simulate one of its submodels by coupling it to coarse-grained versions of all of the other submodels
