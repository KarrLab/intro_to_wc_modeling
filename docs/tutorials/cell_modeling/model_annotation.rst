Model annotation
=========================
In addition to describing models in an understandable format, it is also important to annotate models so that other modelers can understand their biological meaning and provenance. 

Consider the following model of protein expression

.. math::

    \frac{dx}{dx} &= k - \frac{\ln{2}}{\tau} x \\
    k &= 10\,\text{s}^{-1} \\
    \tau &= 18,000\,\text{s} \\

Given just this equation, it is not clear what :math:`x` represents, how the values of :math:`k` and :math:`\tau` where determined, or what algorithm should be used to simulate the model. For example, no information is provided about whether :math:`x` is one specific protein, the entire proteome, an RNA, or a metabolite. To enable others to understand the biological meaning of a model, we must provide additional annotations about the semantic meaning and provenance of each variable, equation, and parameter.


Component-level semantic annotations of species, reactions, and parameters
--------------------------------------------------------------------------
The most common way to communicate the biological meaning of a species or reaction is to annotate the species or reaction with a reference to an external database such as ChEBI for small molecules or UniProt for proteins. SBML supports these annotations as do several software programs including COPASI and VCell.

However, this approach to annotating models via references to external databases a few limitations

* Annotations are limited by the limited content of the databases. For example, ChEBI only contains a fraction of all possible small molecules. 
* Many databases have insufficient resolution to represent variants of species. For example, UniProt does not have separate entries for each splice variants of a gene and even if it did, UniProt could never represent all possible splice variants. Similar, ChEBI does not include every proton isomer of every molecule.
* This approach focuses on species and reaction instances and does not support species or reaction rules.

Instead, we recommend annotating the meanings of species and reactions based on their absolute physical structure. 

* Small molecules: InChI-encoded structures
* DNA, RNA, proteins: Sequences of references to InChI-encoded structures of nucleic and amino acids
* Complexes: Stoichiometric subunit composition
* Reactions: stoichiometries of reactants and products


Model-level semantic annotations
--------------------------------------------------------------------------
Several ontologies have been developed to help modelers describe the semantics of entire models. Below are some of the most useful ontologies for cell modeling. See `BioPortal <bioportal.bioontology.org>`_ for a comprehensive list of ontologies.

* CCO: Cell cycle ontology: can be used to describe cell cycle phases represented by a model
* CL: Cell: can be used to describe cell type represented by a model
* PO: Pathway ontology: can be used to describe the pathways represented by a model

Several software programs can be used to annotate the semantics of entire models. See `http://www.ebi.ac.uk/biomodels-main/annotation <http://www.ebi.ac.uk/biomodels-main/annotation>`_ for a comparison of these programs.

* COPASI
* Saint
* SBMLEditor
* semanticSBML
* SemGen


Model provenance annotations
--------------------------------------------------------------------------
Currently (June 2017), there are no good formats or ontologies for describing the data sources and assumptions used to build models. Currently, we recommend that modelers track this information themselves and embed this information into their model definitions using custom annotations.


Simulation algorithm annotations
--------------------------------------------------------------------------
The KiSAO ontology can be used to describe how to simulate a model. KiSAO is supported by the Simulation Experiment Description Markup Language (SED-ML).


Exercises
--------------------------------------------------------------------------

#. Download a curated model from `BioModels <http://www.ebi.ac.uk/biomodels-main/>`_ and obtain the paper which  reported the model.
#. Remove all of the annotation from the model.
#. Using the paper, databases such as ChEBI and UniProt, and ontologies such as the PO, annotate the semantic meaning of each species and reaction.
#. Using the paper, embed custom annotations which describe the provenance of the model including the assumptions that the modelers made and the data sources that the modelers used to build and calibrate the model.