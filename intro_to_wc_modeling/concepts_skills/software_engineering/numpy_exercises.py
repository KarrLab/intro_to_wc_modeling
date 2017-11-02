""" NumPy exercise answers

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-07-11
:Copyright: 2017, Karr Lab
:License: MIT
"""

import numpy

#########################################
#########################################
# Concatenate two 3x1 arrays of zeros and ones, and get its shape
arr = numpy.concatenate((numpy.zeros((3, 1)), numpy.ones((3, 1))), 1)
assert arr.shape == (3, 2)

#########################################
#########################################
# Select the first column of a random 2x3 array
arr = numpy.random.rand(2, 3)

col = arr[:, 0]
assert col.shape == (2, )

col = arr[:, 0:1]
assert col.shape == (2, 1)

#########################################
#########################################
# Transpose a random 2x3 array into a 3x2 array
arr = numpy.random.rand(2, 3).transpose()
assert arr.shape == (3, 2)

#########################################
#########################################
# Reshape a random 2x3 array into a 3x2 array
arr = numpy.random.rand(2, 3).reshape(3, 2)
assert arr.shape == (3, 2)

#########################################
#########################################
# Create a random 2x3 array and round it
arr = numpy.random.rand(2, 3)
numpy.round(arr)

#########################################
#########################################
# Create a random 100x1 array of Poisson-distributed values with lambda = 10 and calculate its min, max, mean, and standard deviation
arr = numpy.random.poisson(10, (100, 1))
numpy.min(arr)
numpy.max(arr)
numpy.mean(arr)
numpy.std(arr)

#########################################
#########################################
# Calculate the element-wise multiplication of two random arrays of size 3x3
arr1 = numpy.random.rand(3, 3)
arr2 = numpy.random.rand(3, 3)
arr3 = arr1 * arr2
assert arr3.shape == (3, 3)

#########################################
#########################################
# Calculate the matrix multiplication of two random arrays of size 2x3 and 3x4
arr1 = numpy.random.rand(2, 3)
arr2 = numpy.random.rand(3, 4)
arr3 = arr1.dot(arr2)
assert arr3.shape == (2, 4)

#########################################
#########################################
# Check that inf is greater than 1e100
assert numpy.inf > 1e100
