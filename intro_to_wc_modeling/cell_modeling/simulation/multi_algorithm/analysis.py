''' 
Analysis utility functions

@author Jonathan Karr, karr@mssm.edu
@date 3/26/2016
'''

import matplotlib
matplotlib.use('Agg')

from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm.model import Model, Submodel
from intro_to_wc_modeling.cell_modeling.simulation.multi_algorithm.util import N_AVOGADRO
from matplotlib import pyplot, ticker
import numpy as np
import re

def plot(model, time = np.zeros(0), 
    speciesCounts = None, volume = np.zeros(0), extracellularVolume = np.zeros(0),
    selectedSpeciesCompartments = [], 
    yDatas = {},
    units = 'mM', title = '', fileName = ''):

    #convert time to hours
    time = time.copy() / 3600
    
    #create figure
    fig = pyplot.figure()

    #extract data to plot
    if not yDatas:
        yDatas = {}
        for speciesCompartmentId in selectedSpeciesCompartments:
            #extract data
            match = re.match('^(?P<speciesId>[a-z0-9\-_]+)\[(?P<compartmentId>[a-z0-9\-_]+)\]$', speciesCompartmentId, re.I).groupdict()
            speciesId = match['speciesId']
            compartmentId = match['compartmentId']

            if isinstance(model, Model):
                species = model.getComponentById(speciesId)
                compartment = model.getComponentById(compartmentId)
                yData = speciesCounts[species.index, compartment.index, :]
            elif isinstance(model, Submodel):
                yData = speciesCounts[speciesCompartmentId]
            else:
                raise Exception('Invalid model type %s' % model.__class__.__name__)
                
            #scale
            if compartmentId == 'c':
                V = volume
            else:
                V = extracellularVolume
            
            if units == 'pM':
                scale = 1 / N_AVOGADRO / V * 1e12
            elif units == 'nM':
                scale = 1 / N_AVOGADRO / V * 1e9
            elif units == 'uM':
                scale = 1 / N_AVOGADRO / V * 1e6
            elif units == 'mM':
                scale = 1 / N_AVOGADRO / V * 1e3
            elif units == 'M':
                scale = 1 / N_AVOGADRO / V * 1e0
            elif units == 'molecules':
                scale = 1
            else:
                raise Exception('Invalid units "%s"' % units)
                
            yData *= scale
            
            yDatas[speciesCompartmentId] = yData
    
    #plot results    
    yMin = 1e12
    yMax = -1e12
    for label, yData in yDatas.items():
        #update range
        yMin = min(yMin, np.min(yData))
        yMax = max(yMax, np.max(yData))

        #add to plot
        pyplot.plot(time, yData, label=label)
        
    #set axis limits
    pyplot.xlim((0, time[-1]))
    pyplot.ylim((yMin, yMax))
    
    #add axis labels and legend
    if title:
        pyplot.title(title)
    
    pyplot.xlabel('Time (h)')

    if units == 'molecules':
        pyplot.ylabel('Copy number')
    else:
        pyplot.ylabel('Concentration (%s)' % units)
        
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    pyplot.gca().get_yaxis().set_major_formatter(y_formatter)
    
    if len(selectedSpeciesCompartments) > 1:
        pyplot.legend()

    #save
    if fileName:
        fig.savefig(fileName, transparent=True, bbox_inches='tight')
        pyplot.close(fig)
