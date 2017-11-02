How to build a Linux Mint virtual machine with Virtual Box
==========================================================

The goal of this tutorial is to teach you how to build a `Linux Mint <https://linuxmint.com>`_ virtual machine with `Virtual Box <https://www.virtualbox.org>`_.

Linux Mint is an easy to use variant of Linux that is derived from Ubuntu. The key advantage of Linux over Windows is the availability of numerous precompiled packages that can easily be installed using the Mint's package manager.

Virtual machines or VMs are virtual computers that run on top of the operating system of your physical computer. Among other things, virtual machines make it easy to run alternative operating systems or versions of operating systems on your computer. For example, virtual machines make it easy to use Linux on top of a Windows PC without having to create a dual boot, allowing you to use Linux and Windows simultaneously.

Virtual Box is a popular program developed by Oracle that can be used to run virtual machines.

Instructions
------------
#. Download and install Virtual Box from `https://www.virtualbox.org/wiki/Downloads <https://www.virtualbox.org/wiki/Downloads>`_
#. Download Mint Linux, Cinammon, 64-bit from `https://linuxmint.com/download.php <https://linuxmint.com/download.php>`_
#. Run Virtual Box
#. From the Virtual Box main menu, select "Machine" >> "New" and then follow the on screen instructions
    
    #. Enter a name, e.g. "Mint Linux", select Type: "Linux", and select Version: "Ubuntu (64-bit)"
    #. Set the memory size to 4096 MB
    #. Select the option to create a virtual hard disk
        
        #. Select the "VDI" format
        #. Select "Dynamically allocated", 
        #. Set the size to 100 GB
        #. Click "create"

#. Highlight the new virtual machine in Virtual Box, right click on the machine, and select "Settings...". 
#. In the window that opens
    
    #. In "General" >> "Advanced", set "Shared clipboard" to "Bidirectional"
    #. In "System" >> "Processor", set the number of processor to 50% of the maximum and enable "Enable PAE/NX"
    #. In "Display" >> "Screen", enable "Enable 3D video acceleration"

#. Highlight the new virtual machine in Virtual Box, right click on the machine, and select "Start" >> "Normal start".
#. In the window that opens

    #. Select the Mint Linux file that you download in step 2
    #. Click "Start"

#. After the temporary installation OS boots up, double click on the "Install Linux Mint" icon on the desktop
#. In the window that opens

    #. Select your language
    #. Enable "Install third-party software"
    #. Select "Erase disk and install Linux Mint" and select "Use LVM with the new Linux Mint installation"
    #. Select your location
    #. Select your keyboard layout
    #. Enter a user name, computer name, and password
    #. Allow Linux to complete the installation


Additional tutorials
--------------------

There are many other more detailed tutorials on how to build Linux virtual machines

* `How to install Linux Mint as a virtual machine using Windows <http://www.everydaylinuxuser.com/2014/05/how-to-install-linux-mint-as-virtual.html>`_
* `Installing Ubuntu inside Windows using VirtualBox <http://www.psychocats.net/ubuntu/virtualbox>`_
