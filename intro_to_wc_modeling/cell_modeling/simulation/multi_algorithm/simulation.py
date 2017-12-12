'''
Simulates metabolism submodel

@author Jonathan Karr, karr@mssm.edu
@date 3/24/2016
'''

# required libraries
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import analysis
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import model
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm import util
from numpy import random
import numpy as np
import os

# simulation parameters
MODEL_FILENAME = os.path.join(os.path.dirname(__file__), 'Model-Simulation.xlsx')
TIME_STEP = 10  # time step on simulation (s)
TIME_STEP_RECORD = TIME_STEP  # Frequency at which to observe predicted cell state (s)
DEFAULT_OUTPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'docs',
                                        'cell_modeling', 'simulation', 'multi_algorithm_simulation')
RANDOM_SEED = 10000000


def simulate(mdl):
    # simulates model

    # Get FBA, SSA submodels
    ssaSubmodels = []
    for submodel in mdl.submodels:
        if isinstance(submodel, model.SsaSubmodel):
            ssaSubmodels.append(submodel)

    metabolismSubmodel = mdl.getComponentById('Metabolism')

    # get parameters
    cellCycleLength = mdl.getComponentById('cellCycleLength').value

    # seed random number generator to generate reproducible results
    random.seed(RANDOM_SEED)

    # Initialize state
    mdl.calcInitialConditions()

    time = 0  # (s)

    # Initialize history
    timeMax = cellCycleLength  # (s)
    nTimeSteps = int(timeMax / TIME_STEP + 1)
    nTimeStepsRecord = int(timeMax / TIME_STEP_RECORD + 1)
    timeHist = np.linspace(0, timeMax, num=nTimeStepsRecord)

    volumeHist = np.full(nTimeStepsRecord, np.nan)
    volumeHist[0] = mdl.volume

    growthHist = np.full(nTimeStepsRecord, np.nan)
    growthHist[0] = np.log(2) / cellCycleLength

    speciesCountsHist = np.zeros((len(mdl.species), len(mdl.compartments), nTimeStepsRecord))
    speciesCountsHist[:, :, 0] = mdl.speciesCounts

    # Simulate dynamics
    print('Simulating for {} time steps from 0-{} s'.format(nTimeSteps, timeMax))
    for iTime in range(1, nTimeSteps):
        time = iTime * TIME_STEP
        if iTime % 100 == 1:
            print('\tStep = {}, t = {:.1f} s'.format(iTime, time))

        # simulate submodels
        metabolismSubmodel.updateLocalCellState(mdl)
        metabolismSubmodel.calcReactionBounds(TIME_STEP)
        metabolismSubmodel.calcReactionFluxes(TIME_STEP)
        metabolismSubmodel.updateMetabolites(TIME_STEP)
        metabolismSubmodel.updateGlobalCellState(mdl)

        speciesCountsDict = mdl.getSpeciesCountsDict()
        time2 = 0
        while time2 < TIME_STEP:
            time = 0

            # calculate concentrations
            speciesConcentrations = {}
            for id, cnt in speciesCountsDict.items():
                speciesConcentrations[id] = speciesCountsDict[id] / mdl.volume / util.N_AVOGADRO

            # calculate propensities
            totalPropensities = np.zeros(len(ssaSubmodels))
            reactionPropensities = []
            for iSubmodel, submodel in enumerate(ssaSubmodels):
                p = np.maximum(0, model.Submodel.calcReactionRates(submodel.reactions, speciesConcentrations) * mdl.volume * util.N_AVOGADRO)
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

        mdl.setSpeciesCountsDict(speciesCountsDict)

        # update mass, volume
        mdl.calcMass()
        mdl.calcVolume()

        # Record state
        volumeHist[iTime] = mdl.volume
        growthHist[iTime] = mdl.growth
        speciesCountsHist[:, :, iTime] = mdl.speciesCounts

    return (timeHist, volumeHist, growthHist, speciesCountsHist)


def analyzeResults(mdl, time, volume, growth, speciesCounts, output_directory):
    # plot results

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    cellComp = mdl.getComponentById('c')

    totalRna = np.zeros(len(time))
    totalProt = np.zeros(len(time))
    for species in mdl.species:
        if species.type == 'RNA':
            totalRna += speciesCounts[species.index, cellComp.index, :]
        elif species.type == 'Protein':
            totalProt += speciesCounts[species.index, cellComp.index, :]

    analysis.plot(
        model=mdl,
        time=time,
        yDatas={'Volume': volume},
        fileName=os.path.join(output_directory, 'Volume.png')
    )

    analysis.plot(
        model=mdl,
        time=time,
        yDatas={'Growth': growth},
        fileName=os.path.join(output_directory, 'Growth.png')
    )

    analysis.plot(
        model=mdl,
        time=time,
        yDatas={'RNA': totalRna},
        fileName=os.path.join(output_directory, 'Total-RNA.png')
    )

    analysis.plot(
        model=mdl,
        time=time,
        yDatas={'Protein': totalProt},
        fileName=os.path.join(output_directory, 'Total-protein.png')
    )

    analysis.plot(
        model=mdl,
        time=time,
        volume=volume,
        speciesCounts=speciesCounts,
        units='molecules',
        selectedSpeciesCompartments=['ATP[c]', 'CTP[c]', 'GTP[c]', 'UTP[c]'],
        fileName=os.path.join(output_directory, 'NTPs.png')
    )

    analysis.plot(
        model=mdl,
        time=time,
        volume=volume,
        speciesCounts=speciesCounts,
        selectedSpeciesCompartments=['AMP[c]', 'CMP[c]', 'GMP[c]', 'UMP[c]'],
        units='uM',
        fileName=os.path.join(output_directory, 'NMPs.png')
    )

    analysis.plot(
        model=mdl,
        time=time,
        volume=volume,
        speciesCounts=speciesCounts,
        selectedSpeciesCompartments=['ALA[c]', 'ARG[c]', 'ASN[c]', 'ASP[c]'],
        units='uM',
        fileName=os.path.join(output_directory, 'Amino-acids.png')
    )

    analysis.plot(
        model=mdl,
        time=time,
        speciesCounts=speciesCounts,
        units='molecules',
        selectedSpeciesCompartments=['RnaPolymerase-Protein[c]', 'Adk-Protein[c]', 'Apt-Protein[c]', 'Cmk-Protein[c]'],
        fileName=os.path.join(output_directory, 'Proteins.png')
    )


def main(output_directory=DEFAULT_OUTPUT_DIRECTORY):
    """ Run simulation and plot results

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
