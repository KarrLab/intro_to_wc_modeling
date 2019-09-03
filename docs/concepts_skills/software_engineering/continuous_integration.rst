Continuously testing Python code with CircleCI, Coveralls, Code Climate, and the Karr Lab's dashboards
======================================================================================================

To use testing to identify errors as quickly as possible when they are comparatively easy to fix, you should evaluate your tests each time you commit your code. However, this is tedious and it can be time-consuming, particularly as the software gets large and the number of tests grows. Luckily, software engineers have developed tools called continuous integration servers that can automatically test packages each time they are modified.

To use testing effectively on team projects, you should fix broken tests immediately. If you don't fix test failures quickly and instead allow tests to remain broken, you will forfeit your ability to use tests to quickly detect new errors.

We are using the CircleCI cloud-based continuous integration system that has integration with GitHub. Each time you push your code to GitHub, GitHub triggers a "hook" which instructs CircleCI to "build" your code, which includes running all of your tests and notifying you of any errors. While CircleCI is primarily designed to run tests, CircleCI builds are very flexible and can be used to run any arbitrary code upon each trigger. We have used this flexibility to instruct CircleCI to execute the following tasks within each build

* Boot our custom virtual machine
* Install any additional software needed to test the package
* Install the package
* Run all of tests using Python 2 and 3
* Record the coverage of the tests
* Compile the documentation for the package
* Save the results of the tests
* Upload the results of the tests to our test history server
* Upload the coverage of the tests to two online coverage analysis programs, Code Climate and Coveralls


Required packages
-----------------
Execute the following commands to install the packages required for this tutorial::

    sudo curl -o /usr/local/bin/circleci https://circle-downloads.s3.amazonaws.com/releases/build_agent_wrapper/circleci
    sudo chmod +x /usr/local/bin/circleci


Using the CircleCI cloud-based continuous integration system
------------------------------------------------------------
Follow these instructions to use CircleCI to continuously test a GitHub repository

#. Log into `CircleCI <https://circleci.com>`_ using your GitHub account
#. Click on the `Projects` tab
#. Click the `Add Project` button
#. If you see multiple organizations, click on the `KarrLab` button
#. Click the `Follow Project` button for any repository you want to compile and test on CircleCI
#. Add a CircleCI configuration file, ``/path/to/repo/.circleci/config.yml``, to the repository to instruct CircleCI what to execute within each build. This includes the following instructions

    * Which container/virtual machine should be used to run the build. We are using a custom container so that little additional software needs to be installed to test our code. See :ref:`How to build a Ubuntu Linux image with Docker` for more information about how to create and use custom Linux containers.
    * Which GitHub repository to checkout.
    * How to install any additional packages needed to execute the tests.
    * Instructions on how to run the tests and store the results.

    See ``.circleci/config.yml`` for an example and see the `CircleCI documentation <https://circleci.com/docs/2.0/>`_ for more information about configuring CircleCI builds.

In order to upload our test and coverage results to Code Climate, Coveralls, and our lab server, we must set three environment variables in the CircleCI settings for each repository. The values of these variables should be the tokens needed to authenticate with Code Climate, Coveralls, and our lab server. These tokens can be obtained from the corresponding Code Climate and Coveralls projects for each repository.

      * ``CODECLIMATE_REPO_TOKEN``: `obtain from the corresponding Code Climate project`
      * ``COVERALLS_REPO_TOKEN``: `obtain from the corresponding Coveralls project`
      * ``TEST_SERVER_TOKEN``: ``jxdLhmaPkakbrdTs5MRgKD7p``

Optimizing the runtime of CircleCI builds by loading rather than compiling dependent packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are two main mechanisms to decrease the runtime of CircleCI builds by loading rather than compiling dependent packages:

* Use CircleCI's cache to avoid repeatedly compiling the dependent packages.

    This can configured in ``.circleci/config.yml`` as illustrated below::

      - restore_cache:
          keys:
            - cache-vXXX.-{{ .Branch }}-{{ checksum "requirements.txt" }}
            - cache-vXXX-{{ .Branch }}-
            - cache-vXXX-

      ...

      - save_cache:
          key: cache-vXXX-{{ .Branch }}-{{ checksum "requirements.txt" }}

    You can clear these caches by incrementing by the version number ``vXXX`` in ``.circleci/config.yml`` and pushing the updated file to GitHub. This helpful if you want to force the build to compile the dependent package.

* Create your own Docker image which already has the packages compiled

    The Dockerfile for the Docker image that the Karr Lab uses with CircleCI is located at `https://github.com/KarrLab/karr_lab_docker_images/tree/master/build <https://github.com/KarrLab/karr_lab_docker_images/tree/master/build>`_.

    See the :numref:`building_linux_containers` for more information.

The Karr Lab uses both of these mechanisms.

Changing package dependencies for a CircleCI build
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Occasionally, you may need to change the dependencies of a repository. The following recipe can be used to update the PyPI dependencies of a repository:

#. Update the ``pip`` ``requirements.txt`` files which describe the dependencies of the package, its tests, and its documentation.

    * ``./requirements.txt`` describes the dependencies of the package
    * ``./requirements.optional.txt`` describes optional dependencies of the package
    * ``./tests/requirements.txt`` describes the dependencies of the package's tests
    * ``./docs/requirements.txt`` describes the dependencies of the package's documentation, and
    * ``.circleci/requirements.txt`` and ``./docs/requirements.rtd.txt`` tell CircleCI and Read the Docs where to obtain dependencies that are not located in PyPI

#. Commit the changes to the ``requirements.txt`` files to your code repository.

If there are errors in the compilation and/or installation of the new dependencies, you can try rebuilding the build without its cache. As described above, we recommend using CircleCI's cache to avoid repeatedly recompiling dependent packages. The cache avoids recompiling dependent packages by storing them after the first time they are built, and loading them on subsequent builds. You can force CircleCI to create a new cache by incrementing the cache version number ``vXXX`` specified in ``.circleci/config.yml`` and pushing the updated configuration file to your code repository::

    - restore_cache:
        keys:
          - cache-vXXX.-{{ .Branch }}-{{ checksum "requirements.txt" }}
          - cache-vXXX-{{ .Branch }}-
          - cache-vXXX-

    ...

    - save_cache:
        key: cache-vXXX-{{ .Branch }}-{{ checksum "requirements.txt" }}

All other builds that require your package should be configured to update its requirements at the beginning of every build. This can be implementing using pip's ``-U`` option. Note, the Karr Lab's builds are already configured to update their requirements at the beginning of every build.

Debugging CircleCI builds
^^^^^^^^^^^^^^^^^^^^^^^^^
There are four ways to debug CircleCI builds.

* You can iteratively edit and push your ``.circleci/config.yml`` file. However, this is slow because it is not interactive.
* From the CircleCI website, you can rebuild a build with SSH access using the "Rebuild" button at the top-right of the page for the build. After the new build starts, CircleCI will provide you the IP address to SSH into the machine which is running your build. However, this is limited to 2 h, the CircleCI virtual machines are somewhat slow because they are running on top of shared hardware, and any changes you make are not saved to the build image.
* You can use the CircleCI local executor (see below) to emulate CircleCI locally. This is a powerful way to debug CircleCI builds. However, this takes more effort to setup because it requires Docker.
* You can interactively run your code on the Docker build image. This is also a powerful way to debug CircleCI builds. However, this takes more effort to setup because it requires Docker.


Debugging CircleCI builds locally
"""""""""""""""""""""""""""""""""
The CircleCI local executor and interactively running your code on the build image are powerful ways to debug CircleCI builds. Below are instructions for utilizing these approaches.

#. Install Docker (see :numref:`installation`)
#. Install the CircleCI command line tool::

    sudo curl -o /usr/local/bin/circleci https://circle-downloads.s3.amazonaws.com/releases/build_agent_wrapper/circleci
    sudo chmod +x /usr/local/bin/circleci

#. Use the Docker CLI to run a build locally

    .. code-block:: text

      cd /path/to/repo
      circleci build

    Note, this will ignore the Git checkout instructions and instead execute the build instructions using the code in ``/path/to/repo``.

    Note also, if your builds need SSH keys to clone code from a private repository, you will need to prepare a Docker image with the SSH key(s) loaded into it. See this `example Dockerfile <https://github.com/KarrLab/karr_lab_docker_images/blob/master/build/Dockerfile_with_ssh_key>`_.

    See the `CircleCI documentation <https://circleci.com/docs/2.0/local-jobs/>`_ for more information about running builds locally.

#. Use Docker to interactively run the Docker build image::

    docker run -it karrlab/wc_env_dependencies:latest bash

See `https://github.com/KarrLab/karr_lab_docker_images/blob/master/build/test_packages.py <https://github.com/KarrLab/karr_lab_docker_images/blob/master/build/test_packages.py>`_ for a detailed example of how to run builds locally using the CircleCI CLI and Docker.

Code Climate
------------
Follow these instructions to use Code Climate to review the test coverage of a repository

#. Log into `Code Climate <https://codeclimate.com/dashboard>`_ using your GitHub account
#. Click one of the `Add a repository` links
#. Select the desired repository
#. To view the analysis, return to your dashboard and select the package from the dashboard
#. To push coverage data to Code Climate

   #. Open the settings for the package
   #. Navigate to the `Test Coverage` settings
   #. Copy the `Test reporter ID`
   #. Create an environment variable in the corresponding CircleCI build with the key = ``CODECLIMATE_REPO_TOKEN``
      and the value = the value of the `Test reporter ID`

# Once coverage data has been uploaded to Code Climate, you can use the Code Climate GUI to browse the coverage of each module, file, class, method, and line.


Coveralls
---------
Follow these instructions to use Coveralls to review the test coverage of a repository

#. Log into `Coveralls <https://coveralls.io>`_ using your GitHub account
#. Click the `Add repos` button
#. Turn the selected the repository on
#. To push coverage data to Coveralls,

   #. Copy the `repo_token`
   #. Create an environment variable in the corresponding CircleCI build with the key = ``COVERALLS_REPO_TOKEN``
      and the value = the value of `repo_token`

# Once coverage data has been uploaded to Coveralls, you can use the Coveralls GUI to browse the coverage of each module, file, class, method, and line.


Karr Lab test results dashboard (tests.karrlab.org)
---------------------------------------------------
Follow these instructions to use the Karr Lab test results dashboard to review the test results from a CircleCI build

#. Create an environment variable in the CircleCI build with the name ``TEST_SERVER_TOKEN`` and value ``jxdLhmaPkakbrdTs5MRgKD7p``
#. Open `http://tests.karrlab.org  <http://tests.karrlab.org>`_ in you browser. Once tests results have been uploaded to our tests history server, our test results dashboard will allow you to graphically review test results, as well as the performance of each test over time.


Karr Lab software development dashboard (code.karrlab.org)
----------------------------------------------------------
Follow these instructions to use the Karr Lab software development dashboard to monitor the status of a repository

#. SSH into code.karrlab.org
#. Add a repository configuration file to ``/home/karrlab_code/code.karrlab.org/repo/<repo-name>.json``
#. Copy the syntax from the other files in the same directory
#. Open `http://code.karrlab.org <http://code.karrlab.org>`_ in your browser. You should now be able to see the status of the repository, its CircleCI builds, the results of its results, the coverage of its tests, and severals statistics about how many times the repository has been cloned, forked, and downloaded from GitHub and PyPI.
