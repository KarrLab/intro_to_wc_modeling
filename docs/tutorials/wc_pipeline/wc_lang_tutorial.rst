Using the wc_lang Package to Define Whole-Cell Models
=======================================================

This tutorial teaches you how to use the ``wc_lang`` package to define whole-call models.
``wc_lang`` provides a foundation for defining, accessing and manipulating biochemical models composed of species,
reactions, compartments and other parts of a biochemical system.
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
that references instances of ``SpeciesType``, ``Compartment``, and ``Concentration`` which provide
the species' location and concentration.
Adjacency relationships among compartments are implied by reactions that transfer
species among them. However, physical relationships between compartments or their 3D positions
are not represented.

More generally,
a ``wc_lang`` model is a highly-interconnected graph of related Python objects (``obj_model.Model`` instances).
For example, a ``Species`` instance contains ``reaction_participants``,
which references each ``Reaction`` in which the ``Species`` participates.
The graph contain many convenience relationships like this, which make it easy to retrieve useful
related data from anywhere in the graph.

A ``wc_lang`` model also supports some metadata.
A named ``Parameter`` stores an arbitrary value.
Data source used by the model can be recorded in a ``Reference`` which describes a published
source, or a ``CrossReference`` which identifies a biological or chemical
database.

You should think of a ``wc_lang`` model as the description of a model in its initial state because
a ``wc_lang``
description contains much information not required for the simulation of a model, such as
data sources, and lacks any notion of time.


``wc_lang`` Classes Used to Define biochemical Models
------------------------------------------------------

This subsection enumerates all the classes that contain model data in ``wc_lang``.

It is not necessary to import these types; rather, their attributes should be accessed when using a model.

Many classes contain the methods ``serialize()`` and ``deserialize()``, which invert each other.
``serialize()`` converts a Python object instance into a string representation, whereas
``deserialize()`` parses an object's string representation -- as would be stored in a file or spreadsheet
representation of a biochemical model -- into a Python object instance.
``deserialize()`` returns an error when the string representation cannot be parsed into the
Python object.

Static Enumerations
~~~~~~~~~~~~~~~~~~~

Static attributes of these classes are used as attributes of ``wc_lang`` model components.

``TaxonRank``
    The names of biological taxonomic ranks: *domain*, *kingdom*, *phylum*, etc.

``SubmodelAlgorithm``
    The names of algorithms that can solve submodels: *dfba*, *ode*, and *ssa*.

``SpeciesTypeType``
    Types of species types: *metabolite*, *protein*, *dna*, *rna*, and *pseudo_species*.

``RateLawDirection``
    The direction of a reaction rate law: *backward* or *forward*.

``ReferenceType``
    Reference types, such as *article*, *book*, *online*, *proceedings*, etc.

``wc_lang`` Model Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These classes are instantiated as components of a ``wc_lang`` model. All instances of each are
usually
stored in a separate table, either a workbook's worksheet or delimiter-separated file.

``Taxon``
    The taxonomic rank of a model.

``Submodel``
    A part of a whole-cell model which is to be simulated with a particular algorithm from the
    enumeration ``SubmodelAlgorithm``. Each ``Submodel``
    is associated with a ``Compartment`` that contains the ``Species`` it models, and all the reactions
    that transform them. A ``Submodel`` may also have some parameters.

``Compartment``
    A named physical container in the biochemical system being modeled.
    It could represent an organelle or a cell's cytoplasm. It includes an ``initial_volume`` in liters,
    and references to the initial concentrations of  the ``Species`` it contains.
    A compartment can have a semi-permeable membrane, which would be modeled by
    reactions that transform reactant species in the compartment to product species in another compartment.
    These are called membrane-transfer reactions. A membrane-transfer reaction that moves
    species from compartment *x* to compartment *y* implies that *x* and *y* are adjacent.

``SpeciesType``
    The biochemical type of a species. It contains the type's ``name``, ``structure`` -- which is
    represented in InChI for metabolites and as sequences for DNA, RNA, and proteins, ``empirical_formula``,
    ``molecular_weight``, ``charge``, and ``type`` -- which is its ``SpeciesTypeType``.

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
    Attributes for ``k_cat`` and ``k_m`` for a Michaelis–Menten kinetics model are provided, but
    their use isn't required.

``RateLawEquation``
    ``expression`` contains textual a mathematical expression of the rate law provided by the model.
    The expression will be transcoded into a valid Python expression, stored in ``transcoded``, and
    evaluated as Python by a simulator. Evaluating the transcoded expression must produce a number.

    # todo: Expand this:
    The expression is constructed from species names, compartment names, stoichiometric
    reaction coefficients, k_cat and k_m, and Python functions and mathematical operators.
    ``SpeciesType`` and ``Compartment`` names must be valid Python identifiers, and the entire
    expressin must be a valid Python expression.
    A species composed of a ``SpeciesType`` named
    ``species_x`` located in a ``Compartment`` named ``c`` is written ``species_x[c]``. Evaluating
    the rate law converts species into their concentration

``Parameter``
    A ``Parameter`` holds an arbitrary floating point ``value``. It is named, associated with a
    a set of ``submodels``, and should include a modifier indicating the value's ``units``.

``wc_lang`` Model Data Sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These classes specify data sources for the model.

``Reference``
    A ``Reference`` holds a reference to a publication that contains data used in the model.

``CrossReference``
    A ``Reference`` describes a biological or chemical database that provided data for the model.


Using ``wc_lang``
-----------------
``wc_lang`` can be used in several ways. To read and use a model defined in one or more files, follow these steps:

This tutorial assumes that your computer runs Python.

0. Setup the tutorial::

    # In a Unix shell:
    git clone https://github.com/KarrLab/karr_lab_tutorials.git
    cd karr_lab_tutorials/karr_lab_tutorials/wc_pipeline/wc_lang_tutorial
    # install the Python packages required to run this tutorial
    pip install -r wc_pipeline/requirements.txt

You may run this tutorial in the Python interpreter, or execute ``python core.py`` to run all of its code.

..
    # THIS CODE IS DUPLICATED IN karr_lab_tutorials/wc_pipeline/wc_lang_tutorial/core.py
    # KEEP THEM SYNCHRONIZED, OR, BETTER YET, REPLACE THEM WITH A SINGLE FILE AND CONVERSION PROGRAM(S).

1. Import the ``wc_lang`` model reader::

    import os
    from wc_lang.io import Reader

2. Read a model from a file.

Read a model from an Excel workbook. Each worksheet stores the instances of one class (with occasional exceptions
for inline classes)::

    MODEL_FILENAME = os.path.join(os.path.dirname(__file__), 'examples', 'test_wc_lang.xlsx')
    model = Reader().run(MODEL_FILENAME)

A set of delimiter-separated files can store a model. The supported delimiters are *comma* in csv
files or *tab* in tsv files.
Excel workbooks are much easier to edit interactively,
but changes in delimiter-separated files can be tracked by version control systems like Git.
Define a pattern of tsv filenames for the model. Each file stores the instances of one class::

    MODEL_FILENAME_PATTERN = os.path.join(os.path.dirname(__file__), 'examples', 'test_wc_lang-*.tsv')

Make a set of tsv files that contain the same model::

    from wc_lang.io import Writer
    Writer().run(MODEL_FILENAME_PATTERN, model)

Read from tsv files; they must match the glob pattern in ``MODEL_FILENAME_PATTERN``.
The glob matches the names of ``wc_lang`` classes; e.g., ``test_wc_lang-Model.tsv``,
``test_wc_lang-Submodels.tsv``, etc.::

    model_tsv = Reader().run(MODEL_FILENAME_PATTERN)

csv files can be used similarly.

3. Use the model.

For example, list each submodel's id and name::

    for lang_submodel in model.get_submodels():
        print('submodel:', 'id:', lang_submodel.id, 'name:', lang_submodel.name)

We have published the `API documentation <http://www.karrlab.org/>`_ for ``wc_lang`` online.

More usefully, let's access the model and evaluate an aspect of its integrity.

The ``Model`` object in ``wc_lang`` provides a set of convenience methods for accessing a model's elements.
These are:

* ``get_compartments()``

* ``get_species_types()``

* ``get_submodels()``

* ``get_species()``

* ``get_concentrations()``

* ``get_reactions()``

* ``get_rate_laws()``

* ``get_parameters()``

* ``get_references()``

Each of these methods returns a list
containing all of the model's instances of the component type in the method's name.
E.g., ``get_rate_laws()`` returns all of the model's ``RateLaw`` instances.

While the schema ensures that a model provided by ``wc_lang`` has local integrity it does not
evaluate global integrity. For example, a ``wc_lang`` model may associate a compartment with each
submodel and must associate a submodel with each reaction. But it does not ensure that the reactants in
a submodel's reactions are located in the submodel's compartment.
The function ``verify_reactant_compartments`` below evaluates this consistency.
This and other global model
properties must be checked after a model is instantiated. Other such properties include:

* The model does not contain dead-end species which are only consumed or produced

* Reactions are balanced

* Reactions in dynamic submodels contain fully specified rate laws

``verify_reactant_compartments`` uses ``get_submodels()`` to iterate through all submodels. It accesses
each submodel's compartment attribute with ``lang_submodel.compartment``, and
each submodel's reactions with ``lang_submodel.reactions``.::

    def verify_reactant_compartments(model):
        '''Verify that all reactants in each submodel's reactions are in the submodel's compartment

        Returns:
            `list`: errors
        '''
        errors = []
        for lang_submodel in model.get_submodels():
            compartment = lang_submodel.compartment
            if compartment is None:
                errors.append("submodel '{}' must contain a compartment attribute".format(
                    lang_submodel.id))
                continue
            for reaction in lang_submodel.reactions:
                for participant in reaction.participants:
                    if participant.coefficient < 0:     # select reactants
                        if participant.species.compartment != compartment:
                            error = "submodel '{}' models compartment {}, but its reaction {} uses "\
                            "specie {} in another compartment: {}".format(lang_submodel.id,
                                compartment.id, reaction.id, participant.species.species_type.id,
                                participant.species.compartment.id)
                            errors.append(error)
        return errors

    print('\n'.join(verify_reactant_compartments(model)))

Other uses of a ``wc_lang`` model work similarly.

\(c\) Arthur Goldberg, 2017