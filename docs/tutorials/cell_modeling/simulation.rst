Simulation
==========

Simulation descriptions
-----------------------
To simulate a model, we must specify every aspect of the simulation including 

* The model that we want to simulate
* Any modifications of the model that we wish to simulate (e.g. modified parameter values)
* The initial conditions of the simulation
* The desired simulation algorithm
* The parameters of the simulation algorithm such as the initial seed and state of the random number generator

The `Simulation Experiment Description Markup Language <http://sed-ml.org>`_ (SED-ML) is one of the most commonly used languages for describing simulations. SED-ML is primarily designed to describe simulations of XML-based models such as models encoded in CellML and SBML. However, SED-ML can be used to describe the simulation of any model. `Simulation Experiment Specification via a Scala Layer <http://sessl.org>`_ (SESSL) is competing langauage simulation description language. 

Simulation algorithms
---------------------

Flux balance analysis
^^^^^^^^^^^^^^^^^^^^^

Logical models
^^^^^^^^^^^^^^

Ordinary differential equations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stochastic simulation (Gillespie algorithm)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Multi-algorithm simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^

Simulating individual submodels
"""""""""""""""""""""""""""""""
