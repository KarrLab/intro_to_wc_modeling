An introduction to Linux Mint
=============================

Running command line programs
------------------------------------------------
Linux makes it easy to use powerful command line programs. To run a command

#. From the Mint Menu, open the "Terminal" application
#. Type a command such as ``uname`` and then type enter

Note, while command is running you will not be able to run additional commands from that terminal. For example, if you run Firefox by executing ``firefox``, you will not be able to execute additional commands until you close Firefox.

To run additional commands from the same terminal while other commands are running, you must execute commands in the background. This can be done by appending "&" to the end of the command. For example, ``firefox &`` can be used to run Firefox in the background.


Getting help for command line programs
------------------------------------------------
Most command line program provide built in help. For example, these three commands can be used to get help information about Firefox::

    man firefox
    firefox -h
    firefox --help


Installing, upgrading, and uninstalling software
------------------------------------------------
Linux's package manager makes it very easy to install, upgrade, and uninstall packages (i.e. software). This is one of the key advantages of Linux over Windows.

Mint uses `Synaptic <https://help.ubuntu.com/community/SynapticHowto>`_ to manage packages. To search for a package, first open the package manager by running ``synaptic &`` from the command line. In the window that opens, you can search and browse for packages by name and/or category. For example, to install the emacs text editor, search for "emacs", click the checkbox next to the emacs package, select "Mark for installation", accept the installation of emacs' dependencies, and finally click the "Apply" button to install emacs. To upgrade or uninstall emacs, search for "emacs", click the checkbox next to the emacs package, select "Mark for reinstall" or "Mark for uninstall", and finally click the "Apply" button.

Packages can also be installed, upgraded, and uninstalled from the command line using the "apt" command. For example, the following commands can be used to install, upgrade, and remove emacs::
    
    apt-get install emacs
    apt-get upgrade emacs
    apt-get remove emcas

See also the `Ubuntu documentation <https://help.ubuntu.com/community/SynapticHowto>`_ for more information about Synaptic and the `Debian documentation <https://wiki.debian.org/Aptitude>`_ for more information about Aptitude.

Additional tutorials
--------------------
Numerous other Linux tutorials are available

* `http://ryanstutorials.net/linuxtutorial <http://ryanstutorials.net/linuxtutorial/>`_
* `http://linuxcommand.org/learning_the_shell.php <http://linuxcommand.org/learning_the_shell.php>`_
* `https://www.edx.org/course/introduction-linux-linuxfoundationx-lfs101x-1 <https://www.edx.org/course/introduction-linux-linuxfoundationx-lfs101x-1>`_
* `https://www.udacity.com/course/linux-command-line-basics--ud595 <https://www.udacity.com/course/linux-command-line-basics--ud595>`_
