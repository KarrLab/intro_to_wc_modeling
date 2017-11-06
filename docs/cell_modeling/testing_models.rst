Model testing
=============
To generate confidence in a model's predictive capabilities, it is essential to simulate the model and validate that the model makes accurate predictions or debug the until it does make accurate predictions. Formally, model testing can be divided into two stages: `validating` that a model accurate captures the known biology by confirming that the model recapitulates previous experimental observations and 'verifying' that a model accurately predicts previously unknown biology by confirming that the model can accurately predict the outcomes of new experiments.

Because models are engineered software systems, the same approaches that have been developed to validate software can also be used to validate models. This includes both unit testing and formal verification. Within each approach, it is helpful to begin by testing the behaviors of individual model components and then test increasingly large assemblies of components. See :numref:`unit_testing` for model information about how to use unit testing to validate software and models.


Testing composite models
------------------------
Composite models can be tested by first testing each submodel and then testing the combined model. In general, individual submodels should be tested by mocking their interfaces with the other submodels.


Exercise
--------

#. Build a model of the stochastic dynamics of the expression of a single transcript and the cell volume over the cell cycle
#. Simulate the model using the Gillespie algorithm
#. Calibrate the model so that the average transcript copy number doubles on the same time scale as that of the volume
#. Use unit testing to validate that the model is consistent with cell theory (i.e. that the transcript copy number and volume grow at the same time scale)
