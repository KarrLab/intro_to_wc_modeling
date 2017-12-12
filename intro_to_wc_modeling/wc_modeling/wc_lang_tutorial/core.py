''' wc_lang tutorial

:Author: Arthur Goldberg, Arthur.Goldberg@mssm.edu
:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2017-06-19
:Copyright: 2017, Karr Lab
:License: MIT
'''

import inspect
import os
import pkg_resources
import wc_lang.core
import wc_lang.io


def main(examples_dir=os.path.join(os.path.dirname(__file__), 'examples')):
    # todo: synchronize with intro_to_wc_modeling/docs/wc_modeling/wc_lang_tutorial.rst
    ##########################################################################################################
    # THIS CODE IS DUPLICATED IN intro_to_wc_modeling/docs/wc_modeling/wc_lang_tutorial.rst
    # MANUALLY KEEP THEM SYNCHRONIZED, OR, use ``literalinclude`` to link them.
    #
    #   .. literalinclude:: example.py
    #       :language: ruby
    #       :lines: 1,3,5-10,20-
    #       :dedent: 4
    #
    ##########################################################################################################

    ################################################
    # 2. Reading and writing models to/from files
    ################################################

    # ``wc_lang`` can read and write models from specially formatted Excel workbooks in which each worksheet represents a Python class, each row
    # represents a class instance, each column represents an instance attribute, each cell represents the value of an attribute of an
    # instance, and string identifiers are used to indicate relationships among objects

    # This example illustrates how to read a model from an Excel file
    model_filename = pkg_resources.resource_filename('intro_to_wc_modeling', os.path.join(
        'wc_modeling', 'wc_lang_tutorial', 'examples', 'example_model.xlsx'))
    model = wc_lang.io.Reader().run(model_filename)

    # ``wc_lang`` can also read and write models from specially formatted set of delimiter-separated files. `wc_lang`` uses filename glob patterns
    # to indicate sets of delimited files. The supported delimiters are *commas* for .csv files and *tabs* for .tsv files. These files use the same
    # format as the Excel workbook format, except that each worksheet is saved as a separate file.Excel workbooks are easier to edit interactively,
    # but delimiter-separated files are more compatible  with code version control systems such as Git.

    # This example illustrates how to write a model to an set of .tsv files
    if not os.path.isdir(examples_dir):
        os.makedirs(examples_dir)
    model_filename_pattern = os.path.join(examples_dir, 'example_model-*.tsv')
    wc_lang.io.Writer().run(model_filename_pattern, model)

    # This example illustrates how to read a model from a set of .tsv files
    model_from_tsv = wc_lang.io.Reader().run(model_filename_pattern)

    # csv files can be used similarly.

    ################################################
    # 3. Accessing model properties
    ################################################

    #``wc_lang`` models (instances of ``wc_lang.core.Model``) have several attributes
    model.id
    model.name
    model.version
    model.taxon
    model.submodels
    model.compartments
    model.species_types
    model.parameters
    model.references

    # ``wc_lang`` also provides several convenience methods to get all of the elements of a specific type
    # that are part of a model. Each of these methods returns a list of the instances of requested type.
    model.get_compartments()
    model.get_species_types()
    model.get_submodels()
    model.get_species()
    model.get_concentrations()
    model.get_reactions()
    model.get_rate_laws()
    model.get_parameters()
    model.get_references()

    # For example, ``get_submodels`` returns a list of all of the submodels. This can be used to obtain the ids and names of the submodels:
    id_and_names = []
    for submodel in model.get_submodels():
        id_and_names.append('id: {}, name: {}'.format(submodel.id, submodel.name))

    # API documentation for ``wc_lang`` is available at `http://code.karrlab.org <http://code.karrlab.org/>`_.

    #################################################
    # 4. Building models and editing model properties
    #################################################

    # You can also use the classes and methods in ``wc_lang.core`` to programmatically build and edit models

    # The following illustrates how to build a simple model programmatically
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

    # The following illustrates how to edit a model programmatically
    prog_model.id = 'programmatically_created_model'
    prog_model.name = 'Programmatically created model'

    #################################################
    # 5. Comparing and differencing models
    #################################################

    # The ``is_equal`` method determines if two models are semantically equal (i.e. the two models recursively
    # have the same attribute values, ignoring the order of the attributes which has no semantic meaning)
    assert(model.is_equal(model_from_tsv) == True)

    # The ``difference`` method produces a textual description of the differences between two models
    assert(model.difference(model_from_tsv) == '')

    #################################################
    # 6. Normalizing models into a reproducible order
    #################################################

    # Although the attribute order has no semantic meaning, numerical results are sensitive to the attribute order
    # To facilitate reproducible computations, ``wc_lang`` provides a ``normalize`` method which sorts models into
    # a reproducible order
    model.normalize()

    #################################################
    # 7. Complete API
    #################################################

    # The ``wc_lang`` API documentation is available at `http://code.karrlab.org <http://code.karrlab.org/>`_
    inspect.getmembers(wc_lang.core.Model)
    inspect.getmembers(wc_lang.core.Submodel)
    inspect.getmembers(wc_lang.core.Compartment)
    inspect.getmembers(wc_lang.core.SpeciesType)
    inspect.getmembers(wc_lang.core.Reaction)
