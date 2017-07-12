Numerical computing with ``NumPy``
==================================
``NumPy`` is the most popular numerical computing package for Python. The following examples illustrate the basic functionality of ``NumPy``.

Array construction
------------------
.. code-block:: Python

    import numpy
    arr = numpy.array([[1, 2, 3], [4, 5, 6]]) # a 2x3 matrix with elements equal to 1..6
    arr = numpy.empty((2, 2)) # a 2x2 matrix with each element equal to a randomly selected number
    arr = numpy.zeros((2, 2)) # a 2x2 matrix with each element equal to 0.0
    arr = numpy.ones((3, 4)) # a 2x3 matrix with each element equal to 1.0
    arr = numpy.full((2, 3), 2.0) # a 2x3 matrix with each element equal to 2.0

Concatenation
-------------
.. code-block:: Python

    arr1 = numpy.array([...])
    arr2 = numpy.array([...])
    numpy.concatenate(arr1, arr2)

Query the shape of an array
---------------------------
.. code-block:: Python

    arr = numpy.array([...])
    arr.shape()    

Reshaping
---------
.. code-block:: Python

    arr = numpy.array([...])
    arr.reshape((n_row, n_col, ...))

Selection and slicing
---------------------
.. code-block:: Python

    arr = numpy.array([[1, 2, 3], [4, 5, 6]])
    arr[1, 2] # get the value at second row and third column
    arr[0, :] # get the first row
    arr[:, 0] # get the first column

Transposition
-------------
.. code-block:: Python
    
    arr = numpy.array([...])
    arr_trans = arr.transpose()

Algebra
-------
.. code-block:: Python

    arr1 = numpy.array([...])
    arr2 = numpy.array([...])

    arr1 + 2 # element-wise addition
    arr1 - 2 # element-wise subtraction
    arr1 + arr2 # matrix addition
    arr1 - arr2 # matrix subtraction

    2. * arr # scalar multiplication
    arr1 * arr2 # element-wise multiplication
    arr1.dot(arr2) # matrix multiplication

    arr ** 2. # element-wise exponentiation

Trigonometry
------------
.. code-block:: Python

    arr = numpy.array([...])

    numpy.sin(arr) # element-wise sine
    numpy.cos(arr) # element-wise cosine
    numpy.tan(arr) # element-wise tangent
    numpy.asin(arr) # element-wise inverse sin
    numpy.acos(arr) # element-wise inverse cosign
    numpy.atan(arr) # element-wise inverse tangent

Other mathematical functions
----------------------------
.. code-block:: Python

    numpy.sqrt(arr) # element-wise square root
    numpy.ceil() # element-wise ceiling
    numpy.floor() # element-wise floor
    numpy.round() # element-wise round

Data reduction
--------------
.. code-block:: Python

    arr = numpy.array([...])

    arr.all() # determine if all of the values are logically equivalent to `True`
    arr.any() # determine if any of the values are logically equivalent to `True`
    arr.sum() # sum
    arr.mean() # mean
    arr.std() # standard deviation
    arr.var() # variance
    arr.min() # minimum
    arr.max() # maximum

Random number generation
------------------------
.. code-block:: Python

    # set the state of the random number generator to reproducibly generate random values
    numpy.random.seed(1)

    # select a float, randomly between 0 and 1
    numpy.random.rand()

    # select a random integer between 0 and 10
    numpy.random.randint(10)

    # select a random integer according to a Poisson distribution with :math:`\lambda = 2`
    numpy.random.poisson(2.)

NaN and infinity
----------------
.. code-block:: Python

    arr = numpy.array([...])

    numpy.nan
    numpy.isnan(arr)

    numpy.inf
    numpy.isinf(arr)
    numpy.isfinite(arr)


Exercises
---------

* Concatenate two 3x1 arrays of zeros and ones, and get its shape
* Select the first column of a random 2x3 array
* Transpose a random 2x3 array into a 3x2 array
* Reshape a random 2x3 array into a 3x2 array
* Create a random 2x3 array and round it
* Create a random 100x1 array of Poisson-distributed values with lambda = 10 and calculate its min, max, mean, and standard deviation
* Calculate the element-wise multiplication of two random arrays of size 3x3
* Calculate the matrix multiplication of two random arrays of size 2x3 and 3x4
* Check that infinity is greater than :math:`10^{10}`

See `intro_to_wc_modeling/software_engineering/numpy_exercises.py <https://github.com/KarrLab/intro_to_wc_modeling/tree/master/intro_to_wc_modeling/software_engineering/numpy_exercises.py>`_ for solutions to these exercises.


NumPy introduction for MATLAB users
-----------------------------------
The `NumPy documentation <https://docs.scipy.org/doc/numpy-dev/user/numpy-for-matlab-users.html>`_ contains a concise summary of the NumPy analog for each MATLAB function.
