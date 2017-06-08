.. _building_linux_containers:

How to build a Ubuntu Linux container with Docker
=================================================
Docker containers are light weight virtual machines that can be used to run custom environments on top of other machines. Thus, Docker containers are a convenient way to distribute complicated software programs that have numerous dependencies and complicated configurations. We are using Docker containers because CircleCI allows users to use Docker containers to customize the environment used to execute each build. This makes it much easier to install programs into the environment used by CircleCI to run our builds. 

Docker containers are built by compiling Dockerfiles which are explicit instructions on how to build the container. Importantly, this makes Docker containers very transparent.

`Docker Hub <https://hub.docker.com>`_ is a cloud-based system for sharing a distributing Docker containers. Docker Hub allows users to create container repositories, upload containers, make container repositories public, and download containers. CircleCI can build code using any container that is publicly available from Docker Hub.


Required packages
---------------------------
Execute the following commands to install and configure the packages required for this tutorial::
    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       xenial \
       stable"
    sudo apt-get update
    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        docker-ce \
        software-properties-common
    sudo usermod -aG docker $USER


Configuring a container
-----------------------
Docker uses Dockerfiles to configure containers. These files contain several directives

* ``FROM``: the describes the base (and its version) from which to build a container. For example, the value of this derivate could be ``ubuntu:latest`` or a previous iteration of your container.
* ``RUN``: these describe how to install software onto the machine. Because Docker creates layers for each RUN directive, you should use "&" to group related commands together and minimize the number of layers (thus disk space and bandwidth).
* ``CMD``: this tells Docker what the final execution state of the container should be. Often this is set to ``bash``.

See the `Dockerfile reference <https://docs.docker.com/engine/reference/builder/>`_ and `Docker explained <https://www.digitalocean.com/community/tutorials/docker-explained-using-dockerfiles-to-automate-building-of-images>`_ for more information about Dockerfiles.

    
Building a container
--------------------
Once you have configured the container, you can use ``docker build`` to compile the container::

    docker build \
      --tag repository:tag \
      [/path/to/Dockerfile] \
      /path/to/context

    docker build \
      --tag karrlab/build:latest \
      Dockerfile \
      .

If you do not specify a Docker file, then Docker will use the file located at ./Dockerfile. Optionally, you can also use ``docker build`` to tag the versions of containers.


Uploading containers to Docker Hub
----------------------------------
Once you have built a container, you can upload it to Docker Hub

#. Create an account at `Docker Hub <https://hub.docker.com>`_
#. Login into `https://hub.docker.com <https://hub.docker.com>`_
#. Click on the "Create Repository" button
#. Follow the on screen instructions
#. Use the docker command line utility to log into Docker Hub::

    docker login

#. Push the container to the repository and optionally, tag the version of the uploaded container::

    docker push repository[:tag]


Listing existing containers
----------------------------
You can list of all the containers that are already available on your machine by running ``docker images``.


Removing containers
----------------------------
You can remove a container by running the ``rmi`` command::

    docker rmi [repository:tag] [image_id]


Running a container
-------------------
You can use the ``run`` command to run containers::

    docker run -it [repository:tag] [cmd]

If no command is provided, then docker will run the final command in the container's configuration.

Any modifications made to the machine such as installed packages or saved files will not be discarded when the container terminates. When the container is booted up again, the container will start its execution from exactly the same state as all previous executions of the container. This design forces you to use Doxyfiles to explicitly describe container configurations.
