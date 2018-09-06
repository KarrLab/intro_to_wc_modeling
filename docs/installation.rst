.. _installation:

######################################################################
Appendix: Installing the code in this primer and the required packages
######################################################################

Each tutorial outlines how to install all of the necessary software. The following is a consolidated guide to installing all of the software needed for the tutorials.


==========================================================================
Requirements
==========================================================================

Below is a list of all of the packages needed for the tutorials. Note, each tutorial only requires a subset of these packages. Please see the tutorials for information about the packages required for each tutorial.

* CPLEX
* Docker
* Gimp
* Git
* Illustrator
* Inkscape
* libgit2
* Meld
* Open Babel
* Pandoc
* Pip
* Python


==========================================================================
How to install these tutorials
==========================================================================
Run the following command to install the latest version from GitHub::

    git clone git@github.com:KarrLab/intro_to_wc_modeling.git
    pip install -e intro_to_wc_modeling


==========================================================================
Detailed instructions to install the tutorials and all of the requirements
==========================================================================
#. Follow the instructions in :numref:`building_linux_containers` to build a Linux virtual machine
#. Install several packages

    #. Enable the Docker Aptitude repository::

        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        sudo add-apt-repository \
           "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
           xenial \
           stable"
        sudo apt-get update

    #. Install several packages from the Mint repository::

        sudo apt-get install \
            apt-transport-https \
            ca-certificates \
            curl \
            docker-ce \
            gimp \
            git \
            ipython \
            ipython3 \
            inkscape \
            libgnome-keyring-dev \
            libpython-dev \
            libpython3-dev \
            meld \
            mysql-server \
            python \
            python3 \
            python-pip \
            python3-pip \
            software-properties-common \
            texlive \
            zip

    #. Install support for large file in Git repositories::

        curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
        sudo apt-get install git-lfs
        git lfs install

    #. Install `libgit2`::

        wget https://github.com/libgit2/libgit2/archive/v0.26.0.tar.gz -O /tmp/libgit2-0.26.0.tar.gz
        tar -xvvf /tmp/libgit2-0.26.0.tar.gz
        cd /tmp/libgit2-0.26.0
        cmake .
        make
        make install
        ldconfig

        echo "" >> ~/.bashrc
        echo "# libgit2" >> ~/.bashrc
        echo "export LIBGIT2=/usr/local" >> ~/.bashrc

    #. Install Open Babel::

        wget https://github.com/openbabel/openbabel/archive/openbabel-2-4-1.tar.gz -O /tmp/openbabel-2.4.1.tar.gz
        tar -xvvf /tmp/openbabel-2.4.1.tar.gz
        cd openbabel-openbabel-2-4-1
        mkdir build
        cd build
        cmake ..
        make
        make install
        ldconfig

    #. Install the CPLEX optimization package and the CPLEX Python binding

        #. Register for an academic account and download CPLEX from `https://ibm.onthehub.com <https://ibm.onthehub.com>`_

        #. Install CPLEX::

            chmod ugo+x cplex_studio128.linux-x86-64.bin
            ./cplex_studio128.linux-x86-64.bin

        #. Install the Python binding::

            # Python 2.7
            cd /opt/ibm/ILOG/CPLEX_Studio128/cplex/python/2.7/x86-64_linux/
            pip2.7 install .

            # Python 3.6
            cd /opt/ibm/ILOG/CPLEX_Studio128/cplex/python/3.6/x86-64_linux/
            pip3.6 install .

    #. Optionally, install the COIN-OR Cbc optimization package and the CyLP Python binding::

        # set environment variables
        echo "" >> ~/.bashrc
        echo "# COIN-OR: CoinUtils, Cbc" >> ~/.bashrc
        echo "export COIN_INSTALL_DIR=/opt/coin-or/cbc" >> ~/.bashrc
        echo "export PATH=\"\${PATH}:/opt/coin-or/cbc/bin:/opt/coin-or/coinutils/bin\"" >> ~/.bashrc
        echo "export LD_LIBRARY_PATH=\"\${LD_LIBRARY_PATH}:/opt/coin-or/cbc/lib:/opt/coin-or/coinutils/lib\"" >> ~/.bashrc
        ~/.bashrc
        ldconfig

        # CoinUtils
        cd /tmp
        wget --no-check-certificate https://www.coin-or.org/download/source/CoinUtils/CoinUtils-2.10.14.tgz
        tar -xvvf CoinUtils-2.10.14.tgz
        cd CoinUtils-2.10.14
        mkdir build
        cd build
        mkdir -p /opt/coin-or/coinutils
        ../configure -C --prefix=/opt/coin-or/coinutils --enable-gnu-packages
        make
        make install

        # COIN-OR Cbc
        /tmp
        wget --no-check-certificate https://www.coin-or.org/download/source/Cbc/Cbc-2.8.5.tgz
        tar -xvvf Cbc-2.8.5.tgz
        cd Cbc-2.8.5
        mkdir build
        cd build
        ../configure -C --prefix=/opt/coin-or/cbc --enable-gnu-packages
        make
        make install

        # CyLP
        pip install numpy scipy
        pip install git+https://github.com/jjhelmus/CyLP.git@py3#egg=cylp

    #. Optionally, install the Gurobi optimization package and the Gurobi Python binding

        #. Get a Gurobi license from `http://www.gurobi.com <http://www.gurobi.com>`_. Gurobi provides free licenses for academic users.

        #. Install Gurobi::

            apt-get install
            wget http://packages.gurobi.com/7.5/gurobi7.5.2_linux64.tar.gz
            tar xvfz gurobi7.5.2_linux64.tar.gz
            mv gurobi752 /opt/

            echo "" >> ~/.bashrc
            echo "# Gurobi" >> ~/.bashrc
            echo "export GUROBI_HOME=/opt/gurobi752/linux64" >> ~/.bashrc
            echo "export PATH=\"\${PATH}:\${GUROBI_HOME}/bin\"" >> ~/.bashrc
            echo "export LD_LIBRARY_PATH=\"\${LD_LIBRARY_PATH}:\${GUROBI_HOME}/lib\"" >> ~/.bashrc

        #. Use your license to activate Gurobi::

            /opt/gurobi752/linux64/bin/grbgetkey "<license>"

        #. Install the Python binding::

            cd /opt/gurobi752/linux64
            python setup.py install

    #. Optionally, install the MINOS optimization package and the MINOS Python binding:

        #. Request an academic license from `Michael Saunders <mailto:saunders@stanford.edu>`_
        #. Use the following commands to compile MINOS::
            
            apt-get install csh gfortran
            cd /path/to/parent of quadLP.zip
            unzip quadLP.zip
            
            cd quadLP/minos56
            sed -i 's/FC        = gfortran/FC        = gfortran -fPIC/g' Makefile.defs
            make clean
            make
            cd /tmp/quadLP/minos56/test
            make minos
            ./run minos t1diet
            
            ../../../quadLP/qminos56
            sed -i 's/FC        = gfortran/FC        = gfortran -fPIC/g' Makefile.defs
            make clean
            make
            cd /tmp/quadLP/qminos56/test
            make minos
            ./run minos t1diet

        #. Use the following commands to install the MINOS Python binding::
    
            git clone https://github.com/SBRG/solvemepy.git
            cd solvemepy
            cp /path/to/quadLP/minos56/lib/libminos.a ./
            cp /path/to/quadLP/qminos56/lib/libquadminos.a ./
            pip install .

    #. Optionally, install the MOSEK optimization package and the Mosek Python binding:

        #. Request an academic license at `https://license.mosek.com/academic <https://license.mosek.com/academic>`_
        #. Recieve a license by email
        #. Save the license to `${HOME}/mosek/mosek.lic`
        #. Install Mosek::

            cd /tmp
            wget --no-check-certificate https://d2i6rjz61faulo.cloudfront.net/stable/8.1.0.37/mosektoolslinux64x86.tar.bz2
            tar -xvvf mosektoolslinux64x86.tar.bz2
            mv /tmp/mosek /opt/

            echo "" >> ~/.bashrc
            echo "# Mosek" >> ~/.bashrc
            echo "export PATH=\"\${PATH}:/opt/mosek/8/tools/platform/linux64x86/bin\"" >> ~/.bashrc
            echo "export LD_LIBRARY_PATH=\"\${LD_LIBRARY_PATH}:/opt/mosek/8/tools/platform/linux64x86/bin\"" >> ~/.bashrc

        #. Install the Python binding::

            # Python 2.7
            cd /opt/mosek/8/tools/platform/linux64x86/python/2/
            python2.7 setup.py install

            # Python 3.6
            cd /opt/mosek/8/tools/platform/linux64x86/python/3/
            python3.6 setup.py install

    .. commented out because we haven't figured out how to get qpOASES to work with newer versions of Python

        #. Optionally, install the COIN-OR qpOASES optimization package::

            #. Install qpOASES::

                echo "" >> ~/.bashrc
                echo "# COIN-OR: qpOASES" >> ~/.bashrc
                echo "export LD_LIBRARY_PATH=\"\${LD_LIBRARY_PATH}:/opt/coin-or/qpoases/lib\"" >> ~/.bashrc
                ~/.bashrc
                ldconfig

                cd /tmp
                wget --no-check-certificate https://www.coin-or.org/download/source/qpOASES/qpOASES-3.2.1.tgz
                tar -xvvf qpOASES-3.2.1.tgz
                cd qpOASES-3.2.1
                make
                mkdir -p /opt/coin-or/qpoases/lib
                cp bin/libqpOASES.* /opt/coin-or/qpoases/lib
                cp -r include/ /opt/coin-or/qpoases

            #. Install the Python binding::

                cd interfaces/python
                pip install cython numpy
                python setup.py install

    #. Optionally, install the SoPlex optimization package and the SoPlex Python binding:

        #. Download SoPlex 3.1.1 from `http://soplex.zib.de/#download <http://soplex.zib.de/#download>`_
        #. Use the following commands to install SoPlex::

            cd /path/to/parent of soplex-3.1.1.tgz
            tar -xvvf soplex-3.1.1.tgz
            cd soplex-3.1.1
            mkdir build
            cd build
            cmake ..
            make
            make test
            make install

        #. Use the following commands to install the SoPlex Python binding::

            apt-get install libgmp-dev
            pip install cython
            git clone https://github.com/SBRG/soplex_cython.git
            cd soplex_cython
            cp /path/to/soplex-3.1.1.tgz .
            pip install .

    #. Optionally, install the XPRESS optimization package and the XPRESS Python binding

        #. Download and unpack XPRESS::

            cd /tmp
            wget --no-check-certificate https://clientarea.xpress.fico.com/downloads/8.4.4/xp8.4.4_linux_x86_64_setup.tar
            mkdir xp8.4.4_linux_x86_64_setup
            tar -xvvf xp8.4.4_linux_x86_64_setup.tar -C xp8.4.4_linux_x86_64_setup

        #. Get your host id::

            cd /tmp/xp8.4.4_linux_x86_64_setup
            utils/xphostid | grep -m 1 "<id>" | cut -d ">" -f 2 | cut -d "<" -f 1

        #. Use your host id to create a license at `https://app.xpress.fico.com <https://app.xpress.fico.com>`_
        #. Save the license to `/tmp/xpauth.xpr`
        #. Install XPRESS. Note, the standard library directory needs to be added to the library path to prevent the OS from using the versions of libcrypto and libssl provided by XPRESS.::

            cd /tmp/xp8.4.4_linux_x86_64_setup
            ./install.sh

            echo "" >> ~/.bashrc
            echo "# XPRESS" >> ~/.bashrc
            echo "export XPRESSDIR=/opt/xpressmp" >> ~/.bashrc
            echo "export PATH=\"\${PATH}:\${XPRESSDIR}/bin\"" >> ~/.bashrc
            echo "export LD_LIBRARY_PATH=\"\${LD_LIBRARY_PATH}:/lib/x86_64-linux-gnu:\${XPRESSDIR}/lib\"" >> ~/.bashrc
            echo "export CLASSPATH=\"\${CLASSPATH}:\${XPRESSDIR}/lib/xprs.jar:\${XPRESSDIR}/lib/xprb.jar:\${XPRESSDIR}/lib/xprm.jar\"" >> ~/.bashrc
            echo "export XPRESS=\"\${XPRESSDIR}/bin\"" >> ~/.bashrc

        #. Setup the XPRESS Python binding:

            * Add XPRESS to your Python path::

                # Python 2.7
                echo "/opt/xpressmp/lib" | tee /usr/local/lib/python2.7/site-packages/xpress.pth

                # Python 3.6
                echo "/opt/xpressmp/lib" | tee /usr/local/lib/python3.6/site-packages/xpress.pth

            * Save the following package meta data to `/usr/local/lib/python2.7/site-packages/xpress-8.4.4.egg-info` for Python 2.7 and/or `/usr/local/lib/python3.6/site-packages/xpress-8.4.4.egg-info` for Python 3.6::

                Metadata-Version: 1.0
                Name: xpress
                Version: UNKNOWN
                Summary: FICO Xpress-Optimizer Python interface
                Home-page: http://www.fico.com/en/products/fico-xpress-optimization
                Author: Fair Isaac Corporation
                Author-email: UNKNOWN
                License: UNKNOWN
                Description:
                    Xpress-Python interface
                    Copyright (C) Fair Isaac 2016
                    Create, modify, and solve optimization problems in Python using the Xpress Optimization suit
                Platform: UNKNOWN

        Note: If you want to install XPRESS onto a cluster, virtual machine, or docker image, you should first install a XPRESS license server on a static host
        and then install XPRESS using a floating license. See the XPRESS documentation for more information.

    #. Install the Sublime text editor::

        sudo add-apt-repository ppa:webupd8team/sublime-text-3
        sudo apt-get update
        sudo apt-get install sublime-text-installer

    #. Install the `PyCharm IDE <https://www.jetbrains.com/pycharm/download>`_::

        sudo mv ~/Downloads/pycharm-community-2018.2.2.tar.gz /opt/
        sudo tar -xzf pycharm-community-2018.2.2.tar.gz
        cd pycharm-community-2018.2.2/bin
        ./pycharm.sh &

    #. Install the CircleCI command line tool::

        sudo curl -o /usr/local/bin/circleci https://circle-downloads.s3.amazonaws.com/releases/build_agent_wrapper/circleci
        sudo chmod +x /usr/local/bin/circleci

    #. Purchase and install Illustrator


#. Configure the packages

    #. Configure your Git user name and email::

        git config --global user.name "John Doe"
        git config --global user.email "johndoe@example.com"

    #. Configure Git to store your GitHub password::

        cd /usr/share/doc/git/contrib/credential/gnome-keyring
        sudo make
        git config --global credential.helper /usr/share/doc/git/contrib/credential/gnome-keyring/git-credential-gnome-keyring

    #. Add the following to `~/.gitconfig` to configure Git to use meld to visualize differences::

        [diff]
            tool = meld
        [difftool]
            prompt = false
        [difftool "meld"]
            cmd = meld "$LOCAL" "$REMOTE"

    #. Open Sublime and edit the following settings

        * Tools >> Install Package Control
        * Preferences >> Package control >> Install package >> AutoPEP8
        * Preferences >> Key Bindings::

            [
                {"keys": ["ctrl+shift+r"], "command": "auto_pep8", "args": {"preview": false}}
            ]

    #. Open PyCharm and set the following settings to configure PyCharm

        * File >> Settings >> Tools >> Python Integrated Tools >> Default test runner: set to py.test
        * Run >> Edit configurations >> Defaults >> Python tests >> py.test: add additional arguments "--capture=no"
        * Run >> Edit configurations >> Defaults >> Python tests >> Nosetests: add additional arguments "--nocapture"

    #. Configure Docker::

        sudo usermod -aG docker $USER

    #. Install Docker Compose::

        sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose

    #. Optional, setup IDEs such as PyCharm to run code using a Docker image, such as, an image created with *wc_env_manager*.

        * `Jupyter Notebook <https://jupyter-docker-stacks.readthedocs.io/>`_
        * `PyCharm Professional Edition <https://www.jetbrains.com/help/pycharm/docker.html>`_
        * Other IDEs:
            
            #. Install the IDE in a Docker image
            #. Use X11 forwarding to render graphical output from a Docker container to your host. See `Using GUI's with Docker <https://jupyter-docker-stacks.readthedocs.io>`_ for more information.
