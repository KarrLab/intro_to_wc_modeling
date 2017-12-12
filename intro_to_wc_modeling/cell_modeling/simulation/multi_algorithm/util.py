'''
Utility functions

@author Jonathan Karr, karr@mssm.edu
@date 3/22/2016
'''

import numpy as np

N_AVOGADRO = 6.022e23
# Avogadro constant

def nanminimum(x, y):
    return np.where(np.logical_or(np.isnan(y), np.logical_and(x <= y, np.logical_not(np.isnan(x)))), x, y)

def nanmaximum(x, y):
    return np.where(np.logical_or(np.isnan(y), np.logical_and(x >= y, np.logical_not(np.isnan(x)))), x, y)

