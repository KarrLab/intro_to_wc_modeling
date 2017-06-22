############
Installation
############

Each tutorial outlines how to install all of the necessary software. The following is a consolidated guide to installing all of the software needed for the tutorials.


**************************************************************************
Requirements
**************************************************************************
* Docker
* Gimp
* Git
* Illustrator
* Inkscape
* Meld
* Pandoc
* Pip
* Python


**************************************************************************
How to install these tutorials
**************************************************************************
Run the following command to install the latest version from GitHub::

    git clone git@github.com:KarrLab/intro_to_wc_modeling.git    
    pip install -e intro_to_wc_modeling


**************************************************************************
Detailed instructions to install the tutorials and all of the requirements
**************************************************************************
#. :ref:`Build a Mint Linux virtual machine <building_linux_virtual_machines>`
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
            meld \
            mysql-server \
            python \
            python3 \
            python-pip \
            python3-pip \
            software-properties-common \
            texlive

    #. Install support for large file in Git repositories::

        curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
        sudo apt-get install git-lfs
        git lfs install

    #. Install the Sublime text editor::

        sudo add-apt-repository ppa:webupd8team/sublime-text-3
        sudo apt-get update
        sudo apt-get install sublime-text-installer

    #. Install the PyCharm IDE::

        mv ~/Downloads/pycharm-community-2017.1.tar.gz /opt/
        tar -xzf pycharm-community-2017.1.tar.gz
        cd pycharm-community-2017.1
        ./pycharm.sh

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

        * Preferences >> Key Bindings::

            [
                { "keys": ["ctrl+shift+r"], "command": "unbound"}
            ]
            
        * Preferences >> Package control >> Install package >> AutoPEP8
        * Preferences >> Package settings >> AutoPep8 >> Settings-User::

            [{"keys": ["ctrl+shift+r"], "command": "auto_pep8", "args": {"preview": false}}]

    #. Open PyCharm and set the following settings to configure Pycharm

        * File >> Settings >> Tools >> Python Integrated Tools >> Default test runner: set to py.test
        * Run >> Edit configurations >> Defaults >> Python tests >> py.test: add additional arguments "--capture=no"
        * Run >> Edit configurations >> Defaults >> Python tests >> Nosetests: add additional arguments "--nocapture"

    #. Configure docker::

        sudo usermod -aG docker $USER

#. Install these tutorials::

    git clone git@github.com:KarrLab/intro_to_wc_modeling.git
    pip install -e intro_to_wc_modeling
