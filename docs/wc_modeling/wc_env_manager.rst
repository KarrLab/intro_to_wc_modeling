Using *wc_env_manager* build, version, and sharing computing environments for WC modeling
=============================================================================================

WC modeling requires complex computing environments with numerous dependencies. *wc_env_manager* helps modelers and software developers setup customizable computing environments for developing, testing, and running whole-cell (WC) models and WC modeling software. This makes it easy for modelers and software developers to install and configure the numerous dependencies required for WC modeling. This helps modelers and software developers focus on developing WC models and software tools, rather than on installing, configuring, and maintaining complicated dependencies.

In addition, *wc_env_manager* facilitates collaboration by helping WC modelers and software developers share a common base computing environment with third party dependencies. Furthermore, *wc_env_manager* helps software developers anticipate and debug issues in deployment by enabling developers to replicate similar environments to those used to test and deploy WC models and tools in systems such as Amazon EC2, CircleCI, and Heroku.

*wc_env_manager* uses `Docker <https://www.docker.com>`_ to setup a customizable computing environment that contains all of the software packages needed to run WC models and WC modeling software. This includes

    * Required non-Python packages
    * Required Python packages from `PyPI <https://pypi.python.org/pypi>`_ and other sources
    * `WC models and WC modeling tools <https://github.com/KarrLab>`_
    * Optionally, local packages on the user's machine such as clones of these WC models and WC modeling tools

*wc_env_manager* supports both the development and deployment of WC models and WC modeling tools:

    * **Development:** *wc_env_manager* can run WC models and WC modeling software that is located on the user's machine. This is useful for testing WC models and WC modeling software before committing it to GitHub.
    * **Deployment:** *wc_env_manager* can run WC models and WC modeling software from external sources such as GitHub.


How *wc_env_manager* works
-------------------------------------

*wc_env_manager* is based on Docker images and containers which enable virtual environments within all major operating systems including Linux, Mac OSX, and Windows, and the DockerHub repository for versioning and sharing virtual environments.

1. *wc_env_manager* creates a Docker image, *wc_env_dependencies* with the third-party dependencies needed for WC modeling or pulls this image from DockerHub. This image represents an Ubuntu Linux machine.
2. *wc_env_manager* uses this Docker image to create another Docker image, *wc_env* with the WC models, WC modeling tools, and the configuration files and authentication keys needed for WC modeling.
3. *wc_env_manager* uses this image to create a Docker container to run WC models and WC modeling tools. Optionally, the container can have volumes mounted from the host to run code on the host inside the Docker container, which is helpful for using the container to test and debug WC models and tools.

The images and containers created by *wc_env_manager* can be customized using a configuration file.


Installing *wc_env_manager*
---------------------------

First, install the following requirements. See :numref:`installation` for detailed instructions.

* `git <https://git-scm.com/downloads>`_
* `Docker <https://docs.docker.com/install>`_
* `Pip <https://pypi.org/project/pip/>`_ >= 10.0.1
* `Python <https://www.python.org/downloads>`_ >= 3.5

Second, run the following command to install the latest version of *wc_env_manager* from GitHub::

    pip install git+https://github.com/KarrLab/wc_env_manager.git#egg=wc_env_manager


Using *wc_env_manager* to build and share images for WC modeling
----------------------------------------------------------------

Administrators should follow these steps to build and disseminate the *wc_env* and *wc_env_dependencies* images.

#. Create contexts for building the *wc_env* and *wc_env_dependencies* Docker images.
#. Create Dockerfile templates for the *wc_env* and *wc_env_dependencies* Docker images.
#. Set the configuration for *wc_env_manager*.
#. Use *wc_env_manager* to build the *wc_env* and *wc_env_dependencies* Docker images.
#. Use *wc_env_manager* to push the *wc_env* and *wc_env_dependencies* Docker images to DockerHub.


Creating contexts for building the *wc_env* and *wc_env_dependencies* images
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

First, create contexts for building the images. This can include licenses and installers for proprietary software packages.

#. Prepare CPLEX installation

   a. Download CPLEX installer from `https://ibm.onthehub.com <https://ibm.onthehub.com>`_
   b. Save the installer to the base image context
   c. Set the execution bit for the installer by running `chmod ugo+x /path/to/installer`

#. Prepare Gurobi installation

   a. Create license at `http://www.gurobi.com/downloads/licenses/license-center <http://www.gurobi.com/downloads/licenses/license-center>`_
   b. Copy the license to the `gurobi_license` build argument for the base image in the *wc_env_manager* configuration

#. Prepare Mosek installation

   a. Request an academic license at `https://license.mosek.com/academic/ <https://license.mosek.com/academic/>`_
   b. Receive a license by email
   c. Save the license to the context for the base image as `mosek.lic`

#. Prepare XPRESS installation

   a. Install the XPRESS license server on another machine

      i. Download XPRESS from `https://clientarea.xpress.fico.com <https://clientarea.xpress.fico.com>`_
      ii. Use the `xphostid` utility to get your host id
      iii. Use the host id to create a floating license at `https://app.xpress.fico.com <https://app.xpress.fico.com>`_
      iv. Save the license file to the context for the base image as `xpauth.xpr`
      v. Run the installation program and follow the onscreen instructions

   b. Copy the IP address or hostname of the license server to the `xpress_license_server` build argument for the base image in the *wc_env_manager* configuration.
   c. Save the license file to the context for the base image as `xpauth.xpr`.
   d. Edit the server property in the first line of `xpauth.xpr` in the context for the base image. Set the property to the IP address or hostname of the license server.


Creating Dockerfile templates for *wc_env* and *wc_env_dependencies*
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Second, create templates for the Dockerfiles to be rendered by `Jinja <http://jinja.pocoo.org>`_, and save the Dockerfiles within the contexts for the images. The default templates illustrate how to create the Dockerfile templates.

* `/path/to/wc_env_manager/wc_env_manager/assets/base-image/Dockerfile.template`
* `/path/to/wc_env_manager/wc_env_manager/assets/image/Dockerfile.template`


Setting the configuration for *wc_env_manager*
++++++++++++++++++++++++++++++++++++++++++++++

Third, Set the configuration for *wc_env_manager* by creating a configuration file `./wc_env_manager.cfg` following the schema outlined in `/path/to/wc_env_manager/wc_env_manager/config/core.schema.cfg` and the defaults in `/path/to/wc_env_manager/wc_env_manager/config/core.default.cfg`.

* Set the repository and tags for *wc_env* and *wc_env_dependencies*.
* Set the paths for the Dockerfile templates.
* Set the contexts for building the Docker images and the files that should be copied into the images.
* Set the build arguments for building the Docker images. This can include licenses for proprietary software packages.
* Set the WC modeling packages that should be installed into *wc_env*.
* Set your DockerHub username and password.


Building the *wc_env* and *wc_env_dependencies* Docker images
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Use the following command to build the *wc_env* and *wc_env_dependencies* images::

    wc_env_manager build


Pushing the *wc_env* and *wc_env_dependencies* Docker images to DockerHub
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Use the following command to push the *wc_env* and *wc_env_dependencies* images to GitHub::

    wc_env_manager push

Using *wc_env_manager* to create and run Docker containers for WC modeling
--------------------------------------------------------------------------

Developers should follow these steps to build and use WC modeling computing environments (Docker images and containers) to test, debug, and run WC models and WC modeling tools.

#. Use *wc_env_manager* to pull existing WC modeling Docker images
#. Use *wc_env_manager* to create Docker containers with volumes mounted from the host and installations of software packages contained on the house
#. Run models and tools inside the Docker containers created by *wc_env_manager*


Pulling existing Docker images
++++++++++++++++++++++++++++++

First, use the following command to pull existing WC modeling Docker images. This will pull both the base image with third part dependencies, *wc_env_dependencies*, and the image with WC models and modeling tools, *wc_env*.::

  wc_env_manager pull

The following commands can also be used to pull the individual images.::

  wc_env_manager base-image pull
  wc_env_manager image pull


Building containers for WC modeling
+++++++++++++++++++++++++++++++++++

Second, set the configuration for the containers created by *wc_env_manager* by creating a configuration file `./wc_env_manager.cfg` following the schema outlined in `/path/to/wc_env_manager/wc_env_manager/config/core.schema.cfg` and the defaults in `/path/to/wc_env_manager/wc_env_manager/config/core.default.cfg`.

    * Set the host paths that should be mounted into the containers. This should include the root directory of your clones of WC models and WC modeling tools (e.g. map host:~/Documents to container:/root/Documents-Host).
    * Set the WC modeling packages that should be installed into *wc_env*. This should be specified in the pip requirements.txt format and should be specified in terms of paths within the container. The following example illustrates how install clones of *wc_lang* and *wc_utils* mounted from the host into the container.::

        /root/Documents-Host/wc_lang
        /root/Documents-Host/wc_utils

Third, use the following command to use *wc_env* to construct a Docker container.::

  wc_env_manager container build

This will print out the id of the created container.


Using containers to run WC models and WC modeling tools
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

Fourth, use the following command to log in the container.::

  cd /path/to/wc_env_manager
  docker-compose up -d
  docker-compose exec wc_env bash

Fifth, use the integrated WC modeling command line program, `*wc* <https://github.com/KarrLab/wc>`_, to run WC models and WC modeling tools. For example, the following command illustrates how to get help for the *wc* program. See the `*wc* documentation <https://docs.karrlab.org/wc>`_ for more information.::

  container >> wc --help


Using WC modeling computing environments with an external IDE such as PyCharm
-----------------------------------------------------------------------------

The Docker images created with *wc_env_manager* can be used with external integrated development environments (IDEs) such as PyCharm. See the links below for instructions on how to use these tools with Docker images created with *wc_env_manager*.

* `Jupyter Notebook <https://jupyter-docker-stacks.readthedocs.io/>`_
* `PyCharm Professional Edition <https://www.jetbrains.com/help/pycharm/docker.html>`_
* Other IDEs:

    #. Install the IDE in a Docker image
    #. Use X11 forwarding to render graphical output from a Docker container to your host. See `Using GUI's with Docker <https://jupyter-docker-stacks.readthedocs.io>`_ for more information.


Caveats and troubleshooting
-------------------------------------

* Code run in containers created by *wc_env_manager* can create host files and overwrite existing host files. This is because *wc_env_manager* mounts host directories into containers.
* Containers created by *wc_env_manager* can be used to run code located on your host machine. However, using different versions of Python between your host and the Docker containers can create Python caches and compiled Python files that are incompatible between your host and the Docker containers. Before switching between running code on your host your and the Docker containers, you may need to remove all ``__pycache__`` subdirectories and ``*.pyc`` files from host packages mounted into the containers.
* Code run in Docker containers will not have access to the absolute paths of your host and vice-versa. Consequently, arguments that represent absolute host paths or which contain absolute host paths must be mapped from absolute host paths to the equivalent container path. Similarly, outputs which represent or contain absolute container paths must be mapped to the equivalent host paths.
* Running code in containers created with *wc_env_manager* will be slower than running the same code on your host. This is because *wc_env_manager* is based on Docker containers, which add an additional layer of abstraction between your code and your processor.
