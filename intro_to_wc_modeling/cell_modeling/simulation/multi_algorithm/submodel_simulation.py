'''
Simulates metabolism submodel

@author Jonathan Karr, karr@mssm.edu
@date 3/24/2016
'''

# required libraries
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import analysis  # code to analyze simulation results in exercises
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import model  # code for model in exercises
import numpy as np
import os

# simulation parameters
MODEL_FILENAME = os.path.join(os.path.dirname(__file__), 'Model-Simulation.xlsx')
TIME_STEP = 10  # time step on simulation (s)
TIME_STEP_RECORD = TIME_STEP  # Frequency at which to observe predicted cell state (s)
DEFAULT_OUTPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'docs',
                                        'cell_modeling', 'simulation', 'multi_algorithm_submodel_simulation')


def simulate(mdl):
    # simulates model

    # Get metabolism submodel
    submdl = mdl.getComponentById('Metabolism')

    # parameters
    cellCycleLength = mdl.getComponentById('cellCycleLength').value
    rnaHalfLife = mdl.getComponentById('rnaHalfLife').value

    # Initialize state
    mdl.calcInitialConditions()

    time = 0  # (s)
    volume = mdl.volume
    growth = mdl.growth
    speciesCounts = submdl.speciesCounts

    # get data to mock other submodels
    transcriptionSubmdl = mdl.getComponentById('Transcription')
    netTranscriptionReaction = np.zeros((len(mdl.species), len(mdl.compartments)))
    for rxn in transcriptionSubmdl.reactions:
        for part in rxn.participants:
            if part.species.type == 'RNA':
                initCopyNumber = mdl.speciesCounts[part.species.index, part.compartment.index]
        for part in rxn.participants:
            netTranscriptionReaction[part.species.index, part.compartment.index] += part.coefficient * \
                initCopyNumber * (1 + cellCycleLength / rnaHalfLife)

    translationSubmdl = mdl.getComponentById('Translation')
    netTranslationReaction = np.zeros((len(mdl.species), len(mdl.compartments)))
    for rxn in translationSubmdl.reactions:
        for part in rxn.participants:
            if part.species.type == 'Protein':
                initCopyNumber = mdl.speciesCounts[part.species.index, part.compartment.index]
        for part in rxn.participants:
            netTranslationReaction[part.species.index, part.compartment.index] += \
                part.coefficient * initCopyNumber

    rnaDegradationSubmdl = mdl.getComponentById('RnaDegradation')
    netRnaDegradationReaction = np.zeros((len(mdl.species), len(mdl.compartments)))
    for rxn in rnaDegradationSubmdl.reactions:
        for part in rxn.participants:
            if part.species.type == 'RNA':
                initCopyNumber = mdl.speciesCounts[part.species.index, part.compartment.index]
        for part in rxn.participants:
            netRnaDegradationReaction[part.species.index, part.compartment.index] += \
                part.coefficient * initCopyNumber * cellCycleLength / rnaHalfLife

    # Initialize history
    timeMax = cellCycleLength  # (s)
    nTimeSteps = int(timeMax / TIME_STEP + 1)
    nTimeStepsRecord = int(timeMax / TIME_STEP_RECORD + 1)
    timeHist = np.linspace(0, timeMax, num=nTimeStepsRecord)

    volumeHist = np.full(nTimeStepsRecord, np.nan)
    volumeHist[0] = volume

    growthHist = np.full(nTimeStepsRecord, np.nan)
    growthHist[0] = np.log(2) / cellCycleLength

    speciesCountsHist = {}
    for species in submdl.species:
        speciesCountsHist[species.id] = np.full(nTimeStepsRecord, np.nan)
        speciesCountsHist[species.id][0] = speciesCounts[species.id]

    # Simulate dynamics
    print('Simulating for {} time steps from 0-{} s'.format(nTimeSteps, timeMax))
    for iTime in range(1, nTimeSteps):
        time = iTime * TIME_STEP
        if iTime % 100 == 1:
            print('\tStep = {}, t = {:.1f} s'.format(iTime, time))

        # simulate submodel
        submdl.calcReactionBounds(TIME_STEP)
        submdl.calcReactionFluxes(TIME_STEP)
        submdl.updateMetabolites(TIME_STEP)

        # mock other submodels
        submdl.updateGlobalCellState(mdl)

        mdl.speciesCounts += netTranslationReaction * submdl.growth * TIME_STEP
        mdl.speciesCounts += netTranscriptionReaction * submdl.growth * TIME_STEP
        mdl.speciesCounts += netRnaDegradationReaction * submdl.growth * TIME_STEP

        submdl.updateLocalCellState(mdl)

        # update mass, volume
        mdl.calcMass()
        mdl.calcVolume()

        # Record state
        volumeHist[iTime] = mdl.volume
        growthHist[iTime] = mdl.growth
        for species in submdl.species:
            speciesCountsHist[species.id][iTime] = submdl.speciesCounts[species.id]

    return (timeHist, volumeHist, growthHist, speciesCountsHist)


def analyzeResults(mdl, time, volume, growth, speciesCounts, output_directory):
    # plot results

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    submdl = mdl.getComponentById('Metabolism')

    analysis.plot(
        model=submdl,
        time=time,
        yDatas={'Volume': volume},
        fileName=os.path.join(output_directory, 'Volume.png')
    )

    analysis.plot(
        model=submdl,
        time=time,
        yDatas={'Growth': growth},
        fileName=os.path.join(output_directory, 'Growth.png')
    )

    analysis.plot(
        model=submdl,
        time=time,
        volume=volume,
        speciesCounts=speciesCounts,
        units='mM',
        selectedSpeciesCompartments=['ATP[c]', 'CTP[c]', 'GTP[c]', 'UTP[c]'],
        fileName=os.path.join(output_directory, 'NTPs.png')
    )

    analysis.plot(
        model=submdl,
        time=time,
        volume=volume,
        speciesCounts=speciesCounts,
        selectedSpeciesCompartments=['ALA[c]', 'ARG[c]', 'ASN[c]', 'ASP[c]'],
        units='uM',
        fileName=os.path.join(output_directory, 'Amino-acids.png')
    )

    analysis.plot(
        model=submdl,
        time=time,
        volume=volume,
        speciesCounts=speciesCounts,
        units='molecules',
        selectedSpeciesCompartments=['Adk-Protein[c]', 'Apt-Protein[c]', 'Cmk-Protein[c]'],
        fileName=os.path.join(output_directory, 'Proteins.png')
    )


def main(output_directory=DEFAULT_OUTPUT_DIRECTORY):
    """ Run simulation, plot results, and save plots

    Args:
        output_directory (:obj:`str`, optional): directory to save plots        

    Returns:
        :obj:`model.Model`: model
        :obj:`numpy.ndarray`: time
        :obj:`numpy.ndarray`: predicted volume dynamics
        :obj:`numpy.ndarray`: predicted growth rate dynamics
        :obj:`numpy.ndarray`: predicted species counts dynamics
    """
    mdl = model.getModelFromExcel(MODEL_FILENAME)
    time, volume, growth, speciesCounts = simulate(mdl)
    analyzeResults(mdl, time, volume, growth, speciesCounts, output_directory)
    return (mdl, time, volume, growth, speciesCounts)
