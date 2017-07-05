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

  * Which container/virtual machine should be used to run the build. We are using a custom container so that little additional software needs to be installed to test our code. See the `Linux containers tutorial <building_linux_containers>` for more information about how to create and use custom Linux containers.
  * Which GitHub repository to checkout.
  * How to install any additional packages needed to execute the tests.
  * Instructions on how to run the tests and store the results.
  
  See ``.circleci/config.yml`` for an example and see the `CircleCI documentation <https://circleci.com/docs/2.0/>`_ for more information about configuring CircleCI builds.

#. In order to upload our test and coverage results to Code Climate, Coveralls, and our lab server, we must set three environment variables in the CircleCI settings for each repository. The values of these variables should be the tokens needed to authenticate with Code Climate, Coveralls, and our lab server. These tokens can be obtained from the corresponding Code Climate and Coveralls projects for each repository.

    * ``CODECLIMATE_REPO_TOKEN``: `obtain from the corresponding Code Climate project`
    * ``COVERALLS_REPO_TOKEN``: `obtain from the corresponding Coveralls project`
    * ``TEST_SERVER_TOKEN``: ``jxdLhmaPkakbrdTs5MRgKD7p``


Debugging CircleCI builds via SSH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are three ways to debug CircleCI builds. (1) You can make and push changes to your .circleci/config.yml file. However, this is slow because it is not interactive. (2) At the end of each build, you can SSH into the machine that ran the build for up to 30 minutes and interactively debug the build during that time. This is easy to do, but the time is limited to 30 minutes and CircleCI machines are somewhat slow because they are running on top of shared hardware. (3) You can emulate CircleCI locally. This takes more effort to setup, but is the most powerful way to debug CircleCI builds.

To debug builds via SSH, either chose the option to run a build with SSH enable or click the button in the CircleCI page for a build to enable SSH access. In either case, CircleCI will then provide you an IP address and instructions on how to SSH into the machine which ran your build.


Debugging CircleCI builds locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
After installing the CircleCI command line tool, you can use these commands to run a build locally::

  cd /path/to/repo
  circleci build

Note, this will ignore the Git checkout instructions and instead execute the build instructions using the code in ``/path/to/repo``.

See the `CircleCI documentation <https://circleci.com/docs/2.0/local-jobs/>`_ for more information about running builds locally.

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
