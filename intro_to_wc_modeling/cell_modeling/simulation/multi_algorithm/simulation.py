'''
Simulates metabolism submodel

@author Jonathan Karr, karr@mssm.edu
@date 3/24/2016
'''

# required libraries
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import analysis  # code to analyze simulation results in exercises
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm.model import getModelFromExcel, Submodel, SsaSubmodel  # code for model in exercises
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm.util import N_AVOGADRO
from numpy import random
import numpy as np
import os

# simulation parameters
MODEL_FILENAME = os.path.join(os.path.dirname(__file__), 'Model-Simulation.xlsx')
TIME_STEP = 10  # time step on simulation (s)
TIME_STEP_RECORD = TIME_STEP  # Frequency at which to observe predicted cell state (s)
OUTPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'docs', 'tutorials',
                                'cell_modeling', 'simulation', 'multi_algorithm_simulation')
RANDOM_SEED = 10000000


def simulate(model):
    # simulates model

    # Get FBA, SSA submodels
    ssaSubmodels = []
    for submodel in model.submodels:
        if isinstance(submodel, SsaSubmodel):
            ssaSubmodels.append(submodel)

    metabolismSubmodel = model.getComponentById('Metabolism')

    # get parameters
    cellCycleLength = model.getComponentById('cellCycleLength').value

    # seed random number generator to generate reproducible results
    random.seed(RANDOM_SEED)

    # Initialize state
    model.calcInitialConditions()

    time = 0  # (s)

    # Initialize history
    timeMax = cellCycleLength  # (s)
    nTimeSteps = int(timeMax / TIME_STEP + 1)
    nTimeStepsRecord = int(timeMax / TIME_STEP_RECORD + 1)
    timeHist = np.linspace(0, timeMax, num=nTimeStepsRecord)

    volumeHist = np.full(nTimeStepsRecord, np.nan)
    volumeHist[0] = model.volume

    growthHist = np.full(nTimeStepsRecord, np.nan)
    growthHist[0] = np.log(2) / cellCycleLength

    speciesCountsHist = np.zeros((len(model.species), len(model.compartments), nTimeStepsRecord))
    speciesCountsHist[:, :, 0] = model.speciesCounts

    # Simulate dynamics
    print('Simulating for {} time steps from 0-{} s'.format(nTimeSteps, timeMax))
    for iTime in range(1, nTimeSteps):
        time = iTime * TIME_STEP
        if iTime % 100 == 1:
            print('\tStep = {}, t = {:.1f} s'.format(iTime, time))

        # simulate submodels
        metabolismSubmodel.updateLocalCellState(model)
        metabolismSubmodel.calcReactionBounds(TIME_STEP)
        metabolismSubmodel.calcReactionFluxes(TIME_STEP)
        metabolismSubmodel.updateMetabolites(TIME_STEP)
        metabolismSubmodel.updateGlobalCellState(model)

        speciesCountsDict = model.getSpeciesCountsDict()
        time2 = 0
        while time2 < TIME_STEP:
            time = 0

            # calculate concentrations
            speciesConcentrations = {}
            for id, cnt in speciesCountsDict.items():
                speciesConcentrations[id] = speciesCountsDict[id] / model.volume / N_AVOGADRO

            # calculate propensities
            totalPropensities = np.zeros(len(ssaSubmodels))
            reactionPropensities = []
            for iSubmodel, submodel in enumerate(ssaSubmodels):
                p = np.maximum(0, Submodel.calcReactionRates(submodel.reactions, speciesConcentrations) * model.volume * N_AVOGADRO)
                totalPropensities[iSubmodel] = np.sum(p)
                reactionPropensities.append(p)

            # Select time to next reaction from exponential distribution
            dt = random.exponential(1/np.sum(totalPropensities))
            if time2 + dt > TIME_STEP:
                if random.rand() > (TIME_STEP - time2) / dt:
                    break
                else:
                    dt = TIME_STEP - time2

            # Select next reaction
            iSubmodel = random.choice(len(ssaSubmodels), p=totalPropensities / np.sum(totalPropensities))
            iRxn = random.choice(len(reactionPropensities[iSubmodel]), p=reactionPropensities[iSubmodel] / totalPropensities[iSubmodel])

            # update time
            time2 += dt

            # execute reaction
            selectedSubmodel = ssaSubmodels[iSubmodel]
            speciesCountsDict = selectedSubmodel.executeReaction(speciesCountsDict, selectedSubmodel.reactions[iRxn])

        model.setSpeciesCountsDict(speciesCountsDict)

        # update mass, volume
        model.calcMass()
        model.calcVolume()

        # Record state
        volumeHist[iTime] = model.volume
        growthHist[iTime] = model.growth
        speciesCountsHist[:, :, iTime] = model.speciesCounts

    return (timeHist, volumeHist, growthHist, speciesCountsHist)


def analyzeResults(model, time, volume, growth, speciesCounts):
    # plot results

    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    cellComp = model.getComponentById('c')

    totalRna = np.zeros(len(time))
    totalProt = np.zeros(len(time))
    for species in model.species:
        if species.type == 'RNA':
            totalRna += speciesCounts[species.index, cellComp.index, :]
        elif species.type == 'Protein':
            totalProt += speciesCounts[species.index, cellComp.index, :]

    analysis.plot(
        model=model,
        time=time,
        yDatas={'Volume': volume},
        fileName=os.path.join(OUTPUT_DIRECTORY, 'Volume.png')
    )

    analysis.plot(
        model=model,
        time=time,
        yDatas={'Growth': growth},
        fileName=os.path.join(OUTPUT_DIRECTORY, 'Growth.png')
    )

    analysis.plot(
        model=model,
        time=time,
        yDatas={'RNA': totalRna},
        fileName=os.path.join(OUTPUT_DIRECTORY, 'Total RNA.png')
    )

    analysis.plot(
        model=model,
        time=time,
        yDatas={'Protein': totalProt},
        fileName=os.path.join(OUTPUT_DIRECTORY, 'Total protein.png')
    )

    analysis.plot(
        model=model,
        time=time,
        volume=volume,
        speciesCounts=speciesCounts,
        units='molecules',
        selectedSpeciesCompartments=['ATP[c]', 'CTP[c]', 'GTP[c]', 'UTP[c]'],
        fileName=os.path.join(OUTPUT_DIRECTORY, 'NTPs.png')
    )

    analysis.plot(
        model=model,
        time=time,
        volume=volume,
        speciesCounts=speciesCounts,
        selectedSpeciesCompartments=['AMP[c]', 'CMP[c]', 'GMP[c]', 'UMP[c]'],
        units='uM',
        fileName=os.path.join(OUTPUT_DIRECTORY, 'NMPs.png')
    )

    analysis.plot(
        model=model,
        time=time,
        volume=volume,
        speciesCounts=speciesCounts,
        selectedSpeciesCompartments=['ALA[c]', 'ARG[c]', 'ASN[c]', 'ASP[c]'],
        units='uM',
        fileName=os.path.join(OUTPUT_DIRECTORY, 'Amino acids.png')
    )

    analysis.plot(
        model=model,
        time=time,
        speciesCounts=speciesCounts,
        units='molecules',
        selectedSpeciesCompartments=['RnaPolymerase-Protein[c]', 'Adk-Protein[c]', 'Apt-Protein[c]', 'Cmk-Protein[c]'],
        fileName=os.path.join(OUTPUT_DIRECTORY, 'Proteins.png')
    )


def main():
    model = getModelFromExcel(MODEL_FILENAME)
    time, volume, growth, speciesCounts = simulate(model)
    analyzeResults(model, time, volume, growth, speciesCounts)

    # Check if simulation implemented correctly
    volumeChange = (volume[-1] - volume[0]) / volume[0]
    if volumeChange < 0.9 or volumeChange > 1.1:
        raise Exception('Volume should approximately double over the simulation.')
