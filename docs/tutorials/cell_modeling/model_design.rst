Model design
============
Once you have aggregated data to build a model and organized this data into a computable form, the next step of the modeling process is to design your model. The goal of model design is to select the most likely model for a system given everything you know about the system. To avoid overfitting, this selection can be done using cross validation and/or by penalizing larger models to preferentially choose smaller, more parsimonious models. However, it is often difficult to formalize all of your prior knowledge and your confidence in that knowledge and there is often insufficient data to utilize cross validation.

Broadly, there are two families of approaches to designing models: data-driven model design and expert-driven model design. Data-driven model design is a formal mathematical approach to model design that tries to identify the most likely model of a system given prior information about that system. The advantages of data-driven model design are that this approach is rigorous, automated, unbiased, and scalable to large models. However, this approach requires large amounts of data, typically far more than is available and this approach does not leverage heterogeneous prior information effectively. The advantage of expert-driven model design is that it leverages heterogeneous prior information effectively, including information that has not been described formally. However, expert-driven model design can be time-consuming and often leads to models that are biased toward the modeler's preconceptions. 

Due to the limitations of data-driven and expert-driven model design, several groups have developed hybrid model design approaches which automatically generate model design suggestions for modelers to review and accept or reject. For example, Henry et al. developed Model SEED to automatically seed expert-driven FBA metabolism models from models of related organisms, Latendresse et al. developed MetaFlux to seed expert-designed FBA metabolism models from PGDBs, and Kumar et al. developed GapFind to highlight gaps in expert-designed models.

Given that we do not yet have sufficient data to learn models, we must scale expert-driven model building to large models by decomposing models into multiple submodels, programmatically building models from structured sources of prior information, and automatically.


Software tools
--------------
Below are some of the most commonly used model design tools

* Automated model design

    * `bnlearn <http://www.bnlearn.com/>`_
    * `pgmpy <http://pgmpy.org/>`_
    * `scikit-learn <http://scikit-learn.org/>`_

* Manual model design

    * `Cell Collective <https://cellcollective.org/>`_: online, collaborative environment for building logical models
    * `CellDesigner <http://www.celldesigner.org>`_
    * `COPASI <http://copasi.org>`_
    * `JWS Online <http://jjj.biochem.sun.ac.za>`_
    * `PhysioDesigner <http://www.physiodesigner.org>`_    
    * `VirtualCell <http://vcell.org>`_

* Programmatic model design

    * `MetaFlux <http://brg.ai.sri.com/ptools>`_: tool for designing FBA metabolism models for PGDBs
    * `PySB <http://pysb.org/>`_

* Hybrid model design
    
    * `KBase <https://kbase.us/>`_
    * `Model SEED <http://modelseed.org/>`_
    * `RAVEN <http://biomet-toolbox.org/index.php?page=downtools-raven>`_


Exercises
---------

Required software
^^^^^^^^^^^^^^^^^

* `COPASI <http://copasi.org>`_
* `Pathway Tools <http://brg.ai.sri.com/ptools>`_
* Python
* Pip
* Pip packages

    * pgmpy
    * scikit-learn


Expert-driven model design with COPASI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Select a model from BioModels
#. Use the COPASI GUI to recreate your chosen model


PGDB-driven model design with MetaFlux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Download and install `Pathway Tools <http://brg.ai.sri.com/ptools>`_ which contains MetaFlux
#. Download EcoCyc
#. Follow the `MetaFlux tutorial <https://bioinformatics.ai.sri.com/ptools/tutorial/sessions/flux-balance-analysis/fbaTutorialSlides.pdf>`_ and use MetaFlux to construct an FBA model of *Escherichia coli*


Formal model selection
^^^^^^^^^^^^^^^^^^^^^^
See the `sckit-learn tutorial on model selection <http://scikit-learn.org/stable/tutorial/statistical_inference/model_selection.html>`_.


Bayesian network structure learning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
See the `pgmpy tutorial on learning Bayesian networks <https://github.com/pgmpy/pgmpy_notebook/blob/master/notebooks/Learning%20Bayesian%20Networks%20from%20Data.ipynb>`_.
