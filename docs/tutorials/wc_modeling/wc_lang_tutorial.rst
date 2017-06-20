Using the wc_lang package to define whole-cell models
=======================================================

This tutorial teaches you how to use the ``wc_lang`` package to define whole-call models.
``wc_lang`` provides a foundation for defining, accessing and manipulating biochemical models composed of species,
reactions, compartments and other parts of a biochemical system.
It can be used to define models of entire cells, or models of smaller biochemical systems.
``wc_lang`` contains methods to read and write models from two types of files --
spreadsheet workbooks and sets of delimited files. It also includes methods that transform
and summarize models.
``wc_lang`` depends heavily on the ``obj_model`` package which defines a generic language for declaring
interrelated typed data records in Python, transferring them from and to files, and validating their
values.
However, users of ``wc_lang`` do not need to use ``obj_model`` directly.


Semantics of a ``wc_lang`` biochemical Model
----------------------------------------------
A ``wc_lang`` biochemical model represents a biochemical system as ``Species`` (we indicate
classes in ``wc_lang`` by capitalized names in ``fixed-width`` text) which get transformed by reactions.

A ``SpeciesType`` describes a biochemical molecule, including its ``name`` (following Python
convention, attributes
of classes are lowercase names), ``structure``, ``molecular_weight``,
``charge`` and other properties.
The concentration of a ``SpeciesType`` in a compartment is stored by a ``Species`` instance
that references instances of ``SpeciesType``, ``Compartment``, and ``Concentration``, which provide
the species' location and concentration.
A compartment may represent an organelle or a conceptual region of a model.
Adjacency relationships among compartments are implied by reactions that transfer
species among them, but physical relationships between compartments or their 3D positions
are not represented.

The data in
a ``wc_lang`` model is organized in a highly-interconnected graph of related Python objects, each of
which is an ``obj_model.Model`` instance.
For example, a ``Species`` instance contains ``reaction_participants``,
which references each ``Reaction`` in which the ``Species`` participates.
The graph contains many convenience relationships like this, which make it easy to retrieve useful
related data from anywhere in the graph.

A ``wc_lang`` model also supports some metadata.
Named ``Parameter`` entities store arbitrary values, such as input parameters.
Data sources used by the model should be recorded in a ``Reference`` which describes a published
source, or in a ``CrossReference`` which identifies a biological or chemical database.

You should think of a ``wc_lang`` model as the description of a model in its initial state because
a ``wc_lang``
description lacks any notion of time and contains much information not required for the simulation of a model,
such as data sources.


``wc_lang`` Classes Used to Define biochemical Models
------------------------------------------------------

This subsection enumerates all the classes that store data in ``wc_lang`` models.

It is only necessary to import these types when they are being instantiated programmatically.
Typically, their attributes are be accessed when using a model that has been read from file(s).

Many of these classes implement the methods ``serialize()`` and ``deserialize()``.
``deserialize()`` parses an object's string representation -- as would be stored in a text file or spreadsheet
representation of a biochemical model -- into a Python object instance.
Thus, the ``deserialize()`` methods are used when reading models.
``deserialize()`` returns an error when a string representation cannot be parsed into a
Python object.
``serialize()`` converts a Python object instance into a string representation, and is used when
writing a model to a file or files.
``serialize()`` and ``deserialize()`` invert each other.

Static Enumerations
~~~~~~~~~~~~~~~~~~~

Static attributes of these classes are used as attributes of ``wc_lang`` model components.

``TaxonRank``
    The names of biological taxonomic ranks: *domain*, *kingdom*, *phylum*, etc.

``SubmodelAlgorithm``
    The names of algorithms that can integrate submodels: *dfba*, *ode*, and *ssa*.

``SpeciesTypeType``
    Types of species types: *metabolite*, *protein*, *dna*, *rna*, and *pseudo_species*.

``RateLawDirection``
    The direction of a reaction rate law: *backward* or *forward*.

``ReferenceType``
    Reference types, such as *article*, *book*, *online*, *proceedings*, etc.

``wc_lang`` Model Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These classes are instantiated as components of a ``wc_lang`` model.
When a model is stored on disk all the instances of each class are
usually stored in a separate table, either a workbook's worksheet or delimiter-separated file.

``Taxon``
    The taxonomic rank of a model.

``Submodel``
    A part of a whole-cell model which is to be simulated with a particular ``algorithm`` from the
    enumeration ``SubmodelAlgorithm``. Each ``Submodel``
    is associated with a ``Compartment`` that contains the ``Species`` it models, and all the reactions
    that transform them. A ``Submodel`` may also have parameters.

``Compartment``
    A named physical container in the biochemical system being modeled.
    It could represent an organelle, a cell's cytoplasm, or another physical or conceptual structure. 
    It includes an ``initial_volume`` in liters,
    and references to the initial concentrations of the ``Species`` it contains.
    A compartment can have a semi-permeable membrane, which is modeled by
    reactions that transform reactant species in the compartment to product species in another compartment.
    These are called *membrane-transfer* reactions. A membrane-transfer reaction that moves
    species from compartment *x* to compartment *y* implies that *x* and *y* are adjacent.

``SpeciesType``
    The biochemical type of a species. It contains the type's ``name``, ``structure`` -- which is
    represented in InChI for metabolites and as sequences for DNA, RNA, and proteins, ``empirical_formula``,
    ``molecular_weight``, ``charge``, and ``type`` -- which is the species` ``SpeciesTypeType``.

``Species``
    A particular ``SpeciesType`` contained in a particular ``Compartment``.

``Concentration``
    The molar concentration (M) of a species.

``Reaction``
    A biochemical reaction. Each ``Reaction`` belongs to one ``submodel``. It consists of a list
    of the species that participate in the reaction, stored as a list of ``ReactionParticipant``
    in ``participants``.
    A boolean indicates whether the reaction is thermodynamically ``reversible``. A reaction
    that's simulated by a dynamic algorithm, such as an ODE system or SSA, must have a forward
    rate law. It must also have a backward rate law if ``reversible`` is ``True``. Rate laws are
    stored in the ``rate_laws`` list, and their directions are encoded in ``RateLawDirection``
    attributes.

``ReactionParticipant``
    ``ReactionParticipant`` combines a ``Species`` and its stoichiometric reaction coefficient.
    Coefficients are negative for reactants and positive for products.

``RateLaw``
    A rate law contains a textual ``equation`` which stores the mathematical expression of the rate law.
    It contains the ``direction`` of the rate law, encoded with a ``RateLawDirection`` attribute.
    ``k_cat`` and ``k_m`` attributes for a Michaelis–Menten kinetics model are provided, but
    their use isn't required.

``RateLawEquation``
    ``expression`` contains a textual, mathematical expression of the rate law. A rate law can be
    used by more than one ``Reaction``.
    The expression will be transcoded into a valid Python expression, stored in the ``transcoded``
    attribute, and
    evaluated as a Python expression by a simulator. This evaluation must produce a number.

    # todo: Expand this:
    The expression is constructed from species names, compartment names, stoichiometric
    reaction coefficients, k_cat and k_m, and Python functions and mathematical operators.
    ``SpeciesType`` and ``Compartment`` names must be valid Python identifiers, and the entire
    expression must be a valid Python expression.
    A species composed of a ``SpeciesType`` named
    ``species_x`` located in a ``Compartment`` named ``c`` is written ``species_x[c]``. Evaluating
    the rate law converts species into their concentration

``Parameter``
    A ``Parameter`` holds an arbitrary floating point ``value``. It is named, associated with a
    a set of ``submodels``, and should include a modifier indicating the value's ``units``.

``wc_lang`` Model Data Sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These classes record the sources of the model's data.

``Reference``
    A ``Reference`` holds a reference to a publication that contains data used in the model.

``CrossReference``
    A ``Reference`` describes a biological or chemical database that provided data for the model.


Using ``wc_lang``
-----------------
The following tutorial shows several ways to use ``wc_lang``, including 
reading a model defined in one or more files, defining a model programmatically,
and using these models:

..
    # THIS CODE IS DUPLICATED IN intro_to_wc_modeling/wc_modeling/wc_lang_tutorial/core.py
    # KEEP THEM SYNCHRONIZED, OR, BETTER YET, REPLACE THEM WITH A SINGLE FILE AND CONVERSION PROGRAM(S).

#. Install the required software for the tutorial::

    * Python
    * Pip

#. Install the tutorial::

    git clone https://github.com/KarrLab/intro_to_wc_modeling.git
    pip install \
        ipython \
        git+https://github.com/KarrLab/wc_lang.git#egg=wc_lang \
        git+https://github.com/KarrLab/wc_utils.git#egg=wc_utils

#. Change to the directory for this tutorial::

    cd intro_to_wc_modeling/intro_to_wc_modeling/wc_modeling/wc_lang_tutorial

#. Open an interactive python interpreter::
    
    ipython

#. Import the ``os`` and ``wc_lang.io`` modules::

    import os
    import wc_lang.io

#. Read a model from an Excel file::

    ``wc_lang`` can read and write models from specially formatted Excel workbooks in which each worksheet represents a Python class, each row
    represents a class instance, each column represents an instance attribute, each cell represents the value of an attribute of an
    instance, and string identifiers are used to indicate relationships among objects.

    In addition to defining a model, these Excel files should contain all of the annotation needed to understand the biological semantic meaning of
    the model. Ideally, this should include

    * NCBI Taxonomy ID for the taxon
    * Gene Ontology (GO) annotations for each submodel
    * The structure of each species: InChI for small molecules; sequences for polymers
    * Where possible, ChEBI ids for each small molecule
    * Where possible, ids for each gene, transcript, and protein
    * Where possible, EC numbers or KEGG ids for each reaction    
    * `Cell Component Ontology <http://brg.ai.sri.com/CCO>`_ (CCO) annotations for each compartment
    * `Systems Biology Ontology <http://www.ebi.ac.uk/sbo>`_ (SBO) annotations for each parameter
    * The citations which support each model decision
    * PubMed id, DOI, ISBN, or URL for each citation

    This example illustrates how to read a model from an Excel file::

        MODEL_FILENAME = os.path.join('examples', 'example_model.xlsx')
        model = wc_lang.io.Reader().run(MODEL_FILENAME)

    ``wc_lang`` can also read and write a model from a specially formatted set of delimiter-separated files. `wc_lang`` uses filename glob patterns
    to indicate sets of delimited files. The supported delimiters are *commas* for .csv files and *tabs* for .tsv files. These files use the same
    format as the Excel workbook format, except that each worksheet is saved as a separate file.
    Excel workbooks are easier to edit interactively,
    but changes to delimiter-separated files can be tracked in code version control systems such as Git.

    This example illustrates how to write a model to a set of .tsv files::

        MODEL_FILENAME_PATTERN = os.path.join('examples', 'example_model-*.tsv')
        wc_lang.io.Writer().run(MODEL_FILENAME_PATTERN, model)

    This example illustrates how to read this set of .tsv files into a model::

        model_from_tsv = wc_lang.io.Reader().run(MODEL_FILENAME_PATTERN)

    csv files can be used similarly.

#. Access properties of the model::

    ``wc_lang`` models (instances of ``wc_lang.core.Model``) have multiple attributes:

    * ``id``
    * ``name``
    * ``version``
    * ``taxon``
    * ``submodels``
    * ``compartments``
    * ``species_types``
    * ``parameters``
    * ``references``

    ``wc_lang`` also provides several convenience methods to get all of the elements of a specific type
    that are part of a model. Each of these methods returns a list of the instances of requested type.

    * ``get_compartments``
    * ``get_species_types``
    * ``get_submodels``
    * ``get_species``
    * ``get_concentrations``
    * ``get_reactions``
    * ``get_rate_laws``
    * ``get_parameters``
    * ``get_references``

    For example, ``get_submodels`` returns a list of all of the submodels. As illustrated below, this can be 
    used to print the ids and names of the submodels::

        for submodel in model.get_submodels():
            print('id: {}, name: {}'.format(submodel.id, submodel.name))

#. Programmatically build a new model and edit its model properties::

    You can also use the classes and methods in ``wc_lang.core`` to programmatically build and edit models.

    The following illustrates how to build a simple model programmatically::

        prog_model = wc_lang.core.Model(id='programmatic_model', name='Programmatic model')

        submodel = wc_lang.core.Submodel(id='submodel_1', model=prog_model)

        cytosol = wc_lang.core.Compartment(id='c', name='Cytosol')

        atp = wc_lang.core.SpeciesType(id='atp', name='ATP', model=prog_model)
        adp = wc_lang.core.SpeciesType(id='adp', name='ADP', model=prog_model)
        pi = wc_lang.core.SpeciesType(id='pi', name='Pi', model=prog_model)
        h2o = wc_lang.core.SpeciesType(id='h2o', name='H2O', model=prog_model)
        h = wc_lang.core.SpeciesType(id='h', name='H+', model=prog_model)

        atp_hydrolysis = wc_lang.core.Reaction(id='atp_hydrolysis', name='ATP hydrolysis')
        atp_hydrolysis.participants.create(species=wc_lang.core.Species(species_type=atp, compartment=cytosol), coefficient=-1)
        atp_hydrolysis.participants.create(species=wc_lang.core.Species(species_type=h2o, compartment=cytosol), coefficient=-1)
        atp_hydrolysis.participants.create(species=wc_lang.core.Species(species_type=adp, compartment=cytosol), coefficient=1)
        atp_hydrolysis.participants.create(species=wc_lang.core.Species(species_type=pi, compartment=cytosol), coefficient=1)
        atp_hydrolysis.participants.create(species=wc_lang.core.Species(species_type=h, compartment=cytosol), coefficient=1)

    The following illustrates how to edit a model programmatically::

        prog_model.id = 'programmatically_created_model'
        prog_model.name = 'Programmatically created model'

#. Compare and difference ``model`` and ``model_from_tsv``::

    ``wc_lang`` provides methods that determine if two models are semantically equal and report any semantic
    differences between two models. The ``is_equal`` method determines if two models are semantically equal 
    (the two models recursively have the same attribute values, ignoring the order of the attributes which has 
    no semantic meaning). The following code excerpt illustrates how to compare the semantic equality of
    ``model`` and ``model_from_tsv``::

        assert(model.is_equal(model_from_tsv))

    The ``difference`` method produces a textual description of the differences between two models. The following
    code excerpt illustrates how to print the differences between ``model`` and ``model_from_tsv``::

        assert(model.difference(model_from_tsv) == '')

#. Normalize ``model`` into a reproducible order to facilitate reproducible numerical simulations::
    
    The attribute order has no semantic meaning in ``wc_lang``. However, numerical simulation results derived from
    models described in ``wc_lang`` can be sensitive to the attribute order. To facilitate reproducible simulation results,
    ``wc_lang`` provides a ``normalize`` to sort models into a reproducible order.

    The following code excerpt will normalize ``model`` into a reproducible order::

        model.normalize()

#. Please see `http://code.karrlab.org <http://code.karrlab.org/>`_ for documentation of the entire ``wc_lang`` API.
