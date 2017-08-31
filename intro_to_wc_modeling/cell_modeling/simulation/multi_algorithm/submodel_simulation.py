'''
Simulates metabolism submodel

@author Jonathan Karr, karr@mssm.edu
@date 3/24/2016
'''

# required libraries
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import analysis  # code to analyze simulation results in exercises
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm.model import getModelFromExcel  # code for model in exercises
import numpy as np
import os

# simulation parameters
MODEL_FILENAME = os.path.join(os.path.dirname(__file__), 'Model-Simulation.xlsx')
TIME_STEP = 10  # time step on simulation (s)
TIME_STEP_RECORD = TIME_STEP  # Frequency at which to observe predicted cell state (s)
OUTPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'docs', 'tutorials',
                                'cell_modeling', 'simulation', 'multi_algorithm_submodel_simulation')


def simulate(model):
    # simulates model

    # Get metabolism submodel
    submodel = model.getComponentById('Metabolism')

    # parameters
    cellCycleLength = model.getComponentById('cellCycleLength').value
    rnaHalfLife = model.getComponentById('rnaHalfLife').value

    # Initialize state
    model.calcInitialConditions()

    time = 0  # (s)
    volume = model.volume
    growth = model.growth
    speciesCounts = submodel.speciesCounts

    # get data to mock other submodels
    transcriptionSubmodel = model.getComponentById('Transcription')
    netTranscriptionReaction = np.zeros((len(model.species), len(model.compartments)))
    for rxn in transcriptionSubmodel.reactions:
        for part in rxn.participants:
            if part.species.type == 'RNA':
                initCopyNumber = model.speciesCounts[part.species.index, part.compartment.index]
        for part in rxn.participants:
            netTranscriptionReaction[part.species.index, part.compartment.index] += part.coefficient * \
                initCopyNumber * (1 + cellCycleLength / rnaHalfLife)

    translationSubmodel = model.getComponentById('Translation')
    netTranslationReaction = np.zeros((len(model.species), len(model.compartments)))
    for rxn in translationSubmodel.reactions:
        for part in rxn.participants:
            if part.species.type == 'Protein':
                initCopyNumber = model.speciesCounts[part.species.index, part.compartment.index]
        for part in rxn.participants:
            netTranslationReaction[part.species.index, part.compartment.index] += \
                part.coefficient * initCopyNumber

    rnaDegradationSubmodel = model.getComponentById('RnaDegradation')
    netRnaDegradationReaction = np.zeros((len(model.species), len(model.compartments)))
    for rxn in rnaDegradationSubmodel.reactions:
        for part in rxn.participants:
            if part.species.type == 'RNA':
                initCopyNumber = model.speciesCounts[part.species.index, part.compartment.index]
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
    for species in submodel.species:
        speciesCountsHist[species.id] = np.full(nTimeStepsRecord, np.nan)
        speciesCountsHist[species.id][0] = speciesCounts[species.id]

    # Simulate dynamics
    print('Simulating for {} time steps from 0-{} s'.format(nTimeSteps, timeMax))
    for iTime in range(1, nTimeSteps):
        time = iTime * TIME_STEP
        if iTime % 100 == 1:
            print('\tStep = {}, t = {:.1f} s'.format(iTime, time))

        # simulate submodel
        submodel.calcReactionBounds(TIME_STEP)
        submodel.calcReactionFluxes(TIME_STEP)
        submodel.updateMetabolites(TIME_STEP)

        # mock other submodels
        submodel.updateGlobalCellState(model)

        model.speciesCounts += netTranslationReaction * submodel.growth * TIME_STEP
        model.speciesCounts += netTranscriptionReaction * submodel.growth * TIME_STEP
        model.speciesCounts += netRnaDegradationReaction * submodel.growth * TIME_STEP

        submodel.updateLocalCellState(model)

        # update mass, volume
        model.calcMass()
        model.calcVolume()

        # Record state
        volumeHist[iTime] = model.volume
        growthHist[iTime] = model.growth
        for species in submodel.species:
            speciesCountsHist[species.id][iTime] = submodel.speciesCounts[species.id]

    return (timeHist, volumeHist, growthHist, speciesCountsHist)


def analyzeResults(model, time, volume, growth, speciesCounts):
    # plot results

    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    submodel = model.getComponentById('Metabolism')

    analysis.plot(
        model=submodel,
        time=time,
        yDatas={'Volume': volume},
        fileName=os.path.join(OUTPUT_DIRECTORY, 'Volume.png')
    )

    analysis.plot(
        model=submodel,
        time=time,
        yDatas={'Growth': growth},
        fileName=os.path.join(OUTPUT_DIRECTORY, 'Growth.png')
    )

    analysis.plot(
        model=submodel,
        time=time,
        volume=volume,
        speciesCounts=speciesCounts,
        units='mM',
        selectedSpeciesCompartments=['ATP[c]', 'CTP[c]', 'GTP[c]', 'UTP[c]'],
        fileName=os.path.join(OUTPUT_DIRECTORY, 'NTPs.png')
    )

    analysis.plot(
        model=submodel,
        time=time,
        volume=volume,
        speciesCounts=speciesCounts,
        selectedSpeciesCompartments=['ALA[c]', 'ARG[c]', 'ASN[c]', 'ASP[c]'],
        units='uM',
        fileName=os.path.join(OUTPUT_DIRECTORY, 'Amino acids.png')
    )

    analysis.plot(
        model=submodel,
        time=time,
        volume=volume,
        speciesCounts=speciesCounts,
        units='molecules',
        selectedSpeciesCompartments=['Adk-Protein[c]', 'Apt-Protein[c]', 'Cmk-Protein[c]'],
        fileName=os.path.join(OUTPUT_DIRECTORY, 'Proteins.png')
    )


def main():
    model = getModelFromExcel(MODEL_FILENAME)
    time, volume, growth, speciesCounts = simulate(model)
    analyzeResults(model, time, volume, growth, speciesCounts)

    # check simulation immplemented correctly
    growthChange = (growth[-1] - growth[0]) / growth[0]
    if growthChange < 0.9 or growthChange > 1.1:
        raise Exception('Growth rate should double over simulated cell cycle.')

    totalProt = np.zeros(len(time))
    for species in model.getComponentById('Metabolism').species:
        if species.species.type == 'Protein':
            totalProt += speciesCounts[species.id]

    totalProtChange = (totalProt[-1] - totalProt[0]) / totalProt[0]
    if totalProtChange < 0.9 or totalProtChange > 1.1:
        raise Exception('Protein copy numbers should double over simulated cell cycle.')
