Model composition
=================
Abstraction and composition are essential strategies for building large engineered systems such as software programs. Abstraction allows engineers to build complex systems with sophisticated internal details and only expose a few relevant details about their external interfaces to other engineers, allowing other engineers to ignore much of their internal details. Composition enables engineers to build complex systems by combining multiple parts, each which has a simple external interface. In this way, abstraction and composition enable engineers to transform challenging high-dimensional problems into multiple, simpler lower dimensional problems. In particular, abstraction and composition enable teams of engineers to collaboratively build complex systems by enabling individual engineers to independently and simultaneously building individual components.

Because models are engineering software systems, abstraction and composition can also be powerful approaches to build large models. In particular, abstraction and composition can enable teams of modelers to work together to build large models by enabling individual modelers to model individual components. Furthermore, abstraction and composition are reasonable approximations due to the relatively fast dynamics of individual cellular pathways compared to dynamics of interactions between pathways. For example, the time scale of transcription is :math:`10^{1}` s whereas the time scale of the transcriptome, which is the timescale of the impact of RNA on translation, is :math:`10^2` s.

Broadly, there are two types of model composition: composition of mathematically-like models and composition of mathematically-dissimilar models into hybrid or multi-algorithmic models. Mathematically-like models can be merged analytically simply by taking the union of their variables/species and equations/reactions. Mathematically-dissimilar models must be merged computationally by concurrently integrating the individual models. In addition to mathematically and/or computationally merging models, it is often also necessary to align the models to a common namespace and representation.


Model composition procedure
---------------------------
Below are the steps to merging models.

#. Align the models to a common namespace by annotate the species and reactions using common ontologies
#. Make all of the implicit connections among the models implicit. For example, to combine a metabolism model with a signaling model, make ATP an explicit component of the signaling model and update the effective rate constants accordingly.
#. Identify the common species and reactions among the models
#. Align the assumptions, granularity, and mathematical representation of the models

    #. Aligh the assumptions of all of the models. This is typically challenging to do because the assumptions underyling models are rarely explicitly stated.
    #. Align the granularities of all common species and reactions    
    #. Convert all models into explicit time-driven models. For example, convert Boolean models into stochastic models by assuming typical time and copy number scales.
    
#. Mathematically and/or computationally merge the models

    #. Merge all of the mathematically-like models analytically by computing the unions of their species and reactions. For example, ODE models can be merged by taking the union of the state variables and summing the differentials across the models.
    #. Computationally merge the groups of mathematically-dissimilar models by concurrently integrating the models (see the multi-algorithm simulation tutorial).
    
#. Calibrate the combined model. Potentially this could be done be reusing the data that was used to calibrate the individual models. However, this data is rarely published.
#. Validate the combined model. This could also potentially be done using the same data that was used to validate the individual models. However, this data is rarely published.

Unfortunately, it is often challenging to merge published pathway models because published models are often not sufficiently annotated to understand the semantic meaning of each species and reaction and every assumption, because published pathway models often ignore important connections among pathways by lumping them into effective rate constants, and because published pathway models are often calibrated to represented different organisms and environmental conditions. Furthermore, only a few pathways including metabolism, signaling, and cell cycle regulation have good dynamic models that would be useful to merge into whole-cell models.

Instead, we recommend building whole-cell models by designing submodels from scratch explicitly for the purpose of model composition. This ensures that models are described using compatible assumptions, namespaces, granularities, and mathematical representations and calibrated to represent a single common organism and environmental condition.


Software tools
--------------
Several software tools have been developed to help researchers merge models and simulate merge models.

* Model merging: The tools below help users merge models. However, these tools only help users carryout the simplest model merging tasks, namely annotating the semantic meaning of model components and identifying common model components. These software programs do not help models carryout the more complicated tasks of resolving inconsistent assummptions and granularities and recalibrating models.

    * semanticSBML: helps users annotate models and identify common elements
    * SemGen: helps users annotate models and identify common elements

* Numerical simulation of composite multi-algorithmic models

    * E-Cell: multi-algorithmic simulator that uses a nested simulation algorithm
    * iBioSim: implements a hierarchical SSA algorithm that can simulate a specific class of merged stochastic models


Exercises
---------

Merging metabolic models
^^^^^^^^^^^^^^^^^^^^^^^^
In this exercise, you will learn how to merge models by working through the nuances of merging three separately published models of glyolysis.

#. Read the paper which describes the merged model, `Snoep et al., 2006 <https://doi.org/10.1016/j.biosystems.2005.07.006>`_
#. Read the papers which describe the individual models

    * `Cronwright et al., 2002 <http://doi.org/10.1128/AEM.68.9.4448-4456.2002>`_
    * `Martins et al., 2001 <10.1046/j.1432-1327.2001.02304.x>`_
    * `Teusink et al., 2000 <10.1046/j.1432-1327.2000.01527.x>`_
    
* Obtain the original models in SBML format from `JWS online <http://jjj.biochem.sun.ac.za/>`_

    * `Cronwright model <http://jjj.biochem.sun.ac.za/models/cronwright/>`_
    * `Martins model <http://jjj.biochem.sun.ac.za/models/martins/>`_
    * `Teusink model <http://jjj.biochem.sun.ac.za/models/teusink/>`_
    
#. Identify the common species and reactions among the models by annotating the model components against a single namespace
#. Merge the corresponding variables and equations
#. Simulate the merged model
#. Compare your simulation results to those reported in Snoep et al., 2006.


Merging electrophyiological models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In this exercise. you will learn how to merge models by working through the nuances of merging three separately published models of the electrophysiology, calcium dynamics, and tension development of cardiac myocytes.

#. Read the papers which describe the merged model

    * `Terkildsen et al., 2008 <https://doi.org/10.1113/expphysiol.2007.041871>`_
    * `Niederer et al., 2007 <http://dx.doi.org/10.1529/biophysj.106.095463>`_
    * `Neal et al., 2015 <http://doi.org/10.1371/journal.pone.0145621>`_
    
#. Read the papers which describe the original models

    * Pandit et al., 2001 <http://dx.doi.org/10.1016/S0006-3495(01)75943-7>`_
    * Hinch et al., 2004 <http://dx.doi.org/10.1529/biophysj.104.049973>`_
    * Niederer et al., 2006 <http://dx.doi.org/10.1529/biophysj.105.069534>`_

#. Obtain the original models in CellML format from the `CellML model repository <https://models.cellml.org>`_

    * `Pandit model <https://models.cellml.org/exposure/ea62c9c8a502afe364350d353ebf4dd5/pandit_clark_giles_demir_2001_endocardial_cell.cellml/view>`_
    * `Hinch model <https://models.cellml.org/exposure/8e1a590fb82a2cab5284502b430c4a4f/hinch_greenstein_tanskanen_xu_winslow_2004.cellml/view>`_
    * `Niederer model <https://models.cellml.org/exposure/97fb1de5199b1a74c89281db97aecc13/niederer_hunter_smith_2006.cellml/view>`_
    
#. Identify the common species and reactions among the models by annotating the model components against a single namespace
#. Merge the corresponding variables and equations
#. Simulate the merged model
#. Compare your simulation results to those reported in Terkildsen et al., 2008; Niederer et al., 2007; and Neal et al., 2015.
