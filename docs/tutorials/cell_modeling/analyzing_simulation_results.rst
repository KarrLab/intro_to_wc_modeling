Logging simulation results
=====================================================
Broadly, there are two approaches to logging and analyzing simulation results: (a) log specific observables for specific analyses and (b) log all observables and organize the data to facilitate all possible analyses. The first approach is comparatively simple to implement, generates results sets of modest sizes, and doesn't require specialized software for organizing and analyzing simulation results. However, this approach couples simulation and the analysis of simulation results and thus requires modelers to rerun simulations each time they want to run a different analysis. We recommend following the latter approach. This approach decouples simulation from the analysis of simulations which makes it easier for models to explore analyses. This is particularly helpful when you don't yet know what you would like to analyze or where you would like to learn interesting biology from unbiased analysis of simulation data.


Organizing simulation results
=====================================================
To facilitate analysis of large simulation result sets including identifying relevant simulations to analyze, retrieving slices of simulation results, and calculating statistics about simulation results, it is helpful to organize simulation results into a database. Such databases should store simulation results, as well as all of the metadata needed to understand and reproduce the simulation results.

Currently, there are only a few primitive database for simulation results including

* `Bookshelf <http://sbcb.bioch.ox.ac.uk/bookshelf>`_
* `Dynameomics <http://www.dynameomics.org>`_
* `SEEK <https://fair-dom.org/platform/seek>`_
* `WholeCellSimDB <http://www.wholecellsimdb.org>`_


Quickly analyzing large simulation results
=====================================================
As described above, currently there are only a few primitive database for organizing simulation results. In addition to develop better simulation results databases, we must develop better tools for search, extracting, and reducing data stored in such databases. We recommend that such tools be developed using distributed computing frameworks such as `Spark <https://spark.apache.org/>`_.
