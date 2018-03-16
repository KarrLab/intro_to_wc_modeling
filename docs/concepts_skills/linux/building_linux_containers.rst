.. _building_linux_containers:

How to build a Ubuntu Linux image with Docker
=================================================
Docker images are configurable, free-standing computing environments that can be used to create and run custom software on top of an operating system. Unlike virtual machines (VM), images do not contain an operating system. Docker images are a convenient way to distribute complicated software programs that have numerous dependencies and complicated configurations. We are using Docker images because CircleCI allows users to use Docker images to customize the environment used to execute each build. This makes it much easier to install programs into the environment used by CircleCI to run our builds.

Docker images are built by compiling Dockerfiles which are explicit instructions on how to build the image. Importantly, this makes Docker images very transparent.

`Docker Hub <https://hub.docker.com>`_ is a cloud-based system for sharing a distributing Docker images. Docker Hub allows users to create image repositories, upload images, make image repositories public, and download images. CircleCI can build code using any image that is publicly available from Docker Hub.


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
    sudo groupadd docker
	sudo usermod -aG docker $USER
	sudo systemctl enable docker
		
Next, logout and login again.

Run the following to check that you installed Docker correctly::

	docker run hello-world

If you have network access errors, comment out `dns=dnsmasq` in ``/etc/NetworkManager/NetworkManager.conf`` and restart ``network-manager`` and ``docker``::

	sudo service network-manager restart
	sudo service docker restart


Configuring a image
-----------------------
Docker uses Dockerfiles to configure images. These files contain several directives

* ``FROM``: this describes the base (and its version) from which to build a image. For example, the value of this directive could be ``ubuntu:latest`` or a previous iteration of your image.
* ``RUN``: these describe how to install software onto the machine. Because Docker creates layers for each RUN directive, you should use "&" to group related commands together and minimize the number of layers (thus disk space and bandwidth).
* ``CMD``: this tells Docker what the final execution state of the image should be. Often this is set to ``bash``.

See the `Dockerfile reference <https://docs.docker.com/engine/reference/builder/>`_ and `Docker explained <https://www.digitalocean.com/community/tutorials/docker-explained-using-dockerfiles-to-automate-building-of-images>`_ for more information about Dockerfiles.


Building a image
--------------------
Once you have configured the image, you can use ``docker build`` to compile the image::

    docker build \
      --tag repository:tag \
      [/path/to/Dockerfile] \
      /path/to/context

    docker build \
      --tag karrlab/build:latest \
      Dockerfile \
      .

If you do not specify a Docker file, then Docker will use the file located at ./Dockerfile. Optionally, you can also use ``docker build`` to tag the versions of images.


Uploading images to Docker Hub
----------------------------------
Once you have built a image, you can upload it to Docker Hub

#. Create an account at `Docker Hub <https://hub.docker.com>`_
#. Login into `https://hub.docker.com <https://hub.docker.com>`_
#. Click on the "Create Repository" button
#. Follow the on-screen instructions
#. Use the Docker command line utility to log into Docker Hub::

    docker login

#. Push the image to the repository and optionally, tag the version of the uploaded image::

    docker push repository[:tag]


Listing existing images
----------------------------
You can list of all the images that are already available on your machine by running ``docker images``.


Removing images
----------------------------
You can remove a image by running the ``rmi`` command::

    docker rmi [repository:tag] [image_id]


Running an image
-------------------
You can use the ``run`` command to run images::

    docker run -it [repository:tag] [cmd]

If no command is provided, then Docker will run the final command in the image's configuration.

Running a Docker image instantiates a running environment called a container.

Any modifications made to the machine such as installed packages or saved files will not be discarded when the image terminates. When the image is booted up again, the image will start its execution from exactly the same state as the most  recent execution of the image. This design forces you to use Docker files to explicitly describe image configurations.
