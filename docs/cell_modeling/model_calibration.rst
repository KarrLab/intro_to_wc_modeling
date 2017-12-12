Model calibration
=================
Once you have designed the structure of your model, the next step of the modeling process is to calibrate the model to identify/estimate the values of its parameters. Formally, models can be calibrated by identifying the set of parameter values which minimizes the difference between experimental observations and the model's predictions.

Numerous methods have been developed to optimize arbitrary mathematical functions. This includes simple methods such as gradient descent for identifying the optimum of convex functions and scatter search methods for identifying local optima of non-convex problems. Nevertheless, model calibration remains a challenging problem because this often requires optimizing flat high-dimensional non-convex functions, especially to calibrate computationally-expensive, large models.

The goal of this tutorial is to introduce the fundamentals of model calibration.


Key concepts
------------

* Model calibration / model identification / parameter estimation
* Parameter identifiability
* Model calibration formalisms

    * Least squares
    * Maximum likelihood

* Model reduction
* Numerical optimization

    * Gradient descent
    * Scatter search


Calibration data
----------------
Before discussing how to calibrate single-cell models, it is important to note the nature of the data available to calibrate cell models. First, the majority of the data available to calibrate single-cell models directly relate to just one or a few model parameters. This means that most model parameters can be estimated from just a small number of values and, generally, only a few model parameters have to be estimated from physiological data.

Second, although cell models are stochastic and dynamic, most of the data available to build cell models represents the time- and population-average of large groups of cells. Consequently, cell models can be calibrated by calibrating their mean behavior which is significantly less complex and computationally-cheaper problem.


Approximate, multi-stage parameter estimation
---------------------------------------------
In general, calibrating high-dimensional models is computationally-expensive. To reduce the computational cost of parameter estimation, we recommend the following approximate model calibration approach.

#. Do not design parameters whose values have not been measured. Instead, describe that biology qualitatively using fewer parameters.
#. Leverage genomic data to estimate the value of each individual parameter.
#. Generate a reduced model of the time and population average of the full model, decompose this reduced model into reduced pathway submodels, and iteratively optimize the parameters of these reduced submodels until convergence to estimate the joint values of the parameters. The first round of this optimization should be initialized with the parameter values calculated in Step 2.
#. Numerically optimize the parameter values of the full model, starting from the parameter values estimated in Step 3. The primary goal of this final step is to identify parameters who behavior is not adequately captured by the reduced submodels.


Univariate parameter estimates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The first step of this approach is to estimate the value of each individual parameter using the small number of molecular measurements which relate directly to each parameter. For example, we can estimate the transcription initiation rate of each RNA transcript by the ratio of its expression and half-life, each measured by microarray of RNA-seq.


Pathway joint parameter estimates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The second step of this approach to generate a set of reduced pathway submodels to estimate the joint values of the parameters, seeded by the univariate parameter estimates obtained in the previous step.


Model reduction
"""""""""""""""
Because most of the data available to build cells models represents the time- and population-average of large groups of cells, we can calibrate cell models by calibrating reduced models which represent their time- and population average. Such reduced models have the parameters as the corresponding full dynamical model, but they have no time or single-cell dimension.

Broadly, there are two ways to generate such reduced approximate models. (1) We can computationally learn a reduced model by simulating the full model and fitting a function to the results or (2) we can manually reduce the full model by analytically estimating is mean behavior. The latter approach is more biased, but can requires substantially less numerical simulation.


Model decomposition
"""""""""""""""""""
We can further reduce the dimensionality of model calibration by approximating the reduced model as a set of independent pathway submodels and iteratively calibrating these reduced submodels until convergence. Formally, these submodels can be generated using graph clustering. Alternatively, modelers can be asked to manually define these submodels.


Numerical optimization
""""""""""""""""""""""
Once we have generated these reduced model, we can use one of several numerical optimization methods and software tools to estimate the joint values of the parameters of each of the submodels.

* `AMIGO2 <https://sites.google.com/site/amigo2toolbox/home>`_
* `COPASI <http://copasi.org/>`_
* `MEIGO <http://www.iim.csic.es/~gingproc/meigo.html>`_
* `saCeSS <https://bitbucket.org/DavidPenas/sacess-library/>`_


Global joint parameter estimates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Once we have estimated the joint values of the parameters of each of the submodels, we can use the same numerical optimization algorithms outlined above to estimate the joint values of the parameters across the entire model. The main goal of this final step is to estimate parameters who behavior is not adequately captured by the reduced pathway submodels.


Exercise
--------

* Obtain `BioPreDyn-Bench <http://gingproc.iim.csic.es/biopredynbench/index.html>`_, a suite of benchmark model calibration problems
* Use AMIGO and COPASI to calibrate the benchmark *Escherichia coli* model
