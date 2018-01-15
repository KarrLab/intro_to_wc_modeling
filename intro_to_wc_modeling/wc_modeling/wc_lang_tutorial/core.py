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

    ################################################################
    ## This code is used by literalinclude commands in wc_lang_tutorial.rst
    ## It contains many separate examples, each prefixed by comment that delineates the
    ## start of the example and is used by a start-after option in a literalinclude.
    ## The line before each of these comments is:
    ##      'Don't change the next comment - it's used by a literalinclude'
    ## Changes to these comments should be synchronized with changes to wc_lang_tutorial.rst
    ################################################################

    # save the results of example commands so this function can be unit-tested
    results = []

    ################################################
    # 2. Reading and writing models to/from files
    ################################################

    model_filename = os.path.join(examples_dir, 'example_model.xlsx')
    ## Don't change the next comment - it's used by a literalinclude
    # This example illustrates how to read a model from an Excel file
    # 'model_filename' is the name of an Excel file storing a model
    model = wc_lang.io.Reader().run(model_filename)

    results.append("read model: '{}'".format(model.name))

    if not os.path.isdir(examples_dir):
        os.makedirs(examples_dir)
    ## Don't change the next comment - it's used by a literalinclude
    # This example illustrates how to write a model to a set of .tsv files
    # 'examples_dir' is a directory
    model_filename_pattern = os.path.join(examples_dir, 'example_model-*.tsv')
    wc_lang.io.Writer().run(model_filename_pattern, model)

    rv = wc_lang.io.Writer().run(model_filename_pattern, model)
    results.append("write a model to a set of .tsv files: '{}'".format(rv))

    ## Don't change the next comment - it's used by a literalinclude
    # This example illustrates how to read a model from a set of .tsv files
    model_from_tsv = wc_lang.io.Reader().run(model_filename_pattern)

    results.append("read a model from a set of .tsv files: '{}'".format(model_from_tsv.name))

    ################################################
    # 3. Accessing model properties
    ################################################

    ## Don't change the next comment - it's used by a literalinclude
    # ``wc_lang`` models have many attributes
    model.id                # a unique identifier
    model.name              # human readable name
    model.version           # version number
    model.taxon             # taxon of the organism being modeled
    model.submodels         # a list of the model's submodels
    model.compartments      # the model's compartments
    model.species_types     # its species types
    model.parameters        # its parameters
    model.references        # publication sources for the model instance
    model.cross_references  # database sources for the model instance

    results.append("referenced model attributes")

    ## Don't change the next comment - it's used by a literalinclude
    # ``wc_lang`` also provides many convenience methods
    model.get_compartments()
    model.get_species_types()
    model.get_submodels()
    model.get_species()
    model.get_concentrations()
    model.get_reactions()
    model.get_biomass_reactions()
    model.get_rate_laws()
    model.get_parameters()
    model.get_references()

    results.append("referenced model convenience methods")

    ## Don't change the next comment - it's used by a literalinclude
    # ``get_reactions()`` returns a list of all of the reactions in a model's submodels
    reaction_identification = []
    for reaction in model.get_reactions():
        reaction_identification.append('submodel name: {}, reaction id: {}'.format(
            reaction.submodel.name, reaction.id))

    results.append("get_reactions entry 0: '{}'".format(reaction_identification[0]))

    #################################################
    # 4. Building models and editing model properties
    #################################################

    ## Don't change the next comment - it's used by a literalinclude
    # The following illustrates how to build a simple model programmatically
    # create a model with one submodel and one compartment
    prog_model = wc_lang.core.Model(id='programmatic_model', name='Programmatic model')

    submodel = wc_lang.core.Submodel(id='submodel_1', model=prog_model)

    cytosol = wc_lang.core.Compartment(id='c', name='Cytosol')

    # create 5 species types
    atp = wc_lang.core.SpeciesType(id='atp', name='ATP', model=prog_model)
    adp = wc_lang.core.SpeciesType(id='adp', name='ADP', model=prog_model)
    pi = wc_lang.core.SpeciesType(id='pi', name='Pi', model=prog_model)
    h2o = wc_lang.core.SpeciesType(id='h2o', name='H2O', model=prog_model)
    h = wc_lang.core.SpeciesType(id='h', name='H+', model=prog_model)

    # create an 'ATP hydrolysis' reaction with 2 reactants and 3 products
    atp_hydrolysis = wc_lang.core.Reaction(id='atp_hydrolysis', name='ATP hydrolysis')
    atp_hydrolysis.participants.create(
        species=wc_lang.core.Species(species_type=atp, compartment=cytosol), coefficient=-1)
    atp_hydrolysis.participants.create(
        species=wc_lang.core.Species(species_type=h2o, compartment=cytosol), coefficient=-1)
    atp_hydrolysis.participants.create(
        species=wc_lang.core.Species(species_type=adp, compartment=cytosol), coefficient=1)
    atp_hydrolysis.participants.create(
        species=wc_lang.core.Species(species_type=pi, compartment=cytosol), coefficient=1)
    atp_hydrolysis.participants.create(
        species=wc_lang.core.Species(species_type=h, compartment=cytosol), coefficient=1)
    # The previous illustrates how to build a simple model programmatically
    ## Don't change the previous comment - it's used by a literalinclude

    results.append("created model: '{}'".format(prog_model.name))

    ## Don't change the next comment - it's used by a literalinclude
    # The attribues that can be initialized when a ``wc_lang.BaseModel`` class is instantiated
    wc_lang.core.Model.Meta.attributes.keys()
    wc_lang.core.Submodel.Meta.attributes.keys()
    wc_lang.core.SpeciesType.Meta.attributes.keys()
    wc_lang.core.Compartment.Meta.attributes.keys()

    ## Don't change the next comment - it's used by a literalinclude
    # The following illustrates how to edit a model programmatically
    atp_hydrolysis.comments = 'example comments'
    atp_hydrolysis.reversible = False

    #################################################
    # 5. Completing and validating models
    #################################################

    ## Don't change the next comment - it's used by a literalinclude
    # This example illustrates how to validate ``prog_model``
    prog_model.validate()

    rv = prog_model.validate()
    results.append("validate model: '{}'".format(rv))

    # print(atp_hydrolysis.participants[0])
    # TODO: make this work print(atp_hydrolysis.participants[0].reaction)

    #################################################
    # 6. Comparing and differencing models
    #################################################

    ## Don't change the next comment - it's used by a literalinclude
    # compare the semantic equality of ``model`` and ``model_from_tsv``
    assert(model.is_equal(model_from_tsv) == True)

    ## Don't change the next comment - it's used by a literalinclude
    # produces a textual description of the differences between two models
    assert(model.difference(model_from_tsv) == '')

    #################################################
    # 7. Normalizing models into a reproducible order
    #################################################

    ## Don't change the next comment - it's used by a literalinclude
    # The following code excerpt will normalize ``model`` into a reproducible order
    model.normalize()

    rv = model.normalize()
    results.append("normalize model: '{}'".format(rv))

    return results

if __name__ == '__main__':
    main()