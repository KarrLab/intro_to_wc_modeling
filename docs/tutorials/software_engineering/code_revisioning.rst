.. _code_revisioning:

How to revision code with Git, GitHub, and Meld
===============================================

This tutorial will teach you how to use Git, GitHub, and Meld to manage code revisions/versions/changes.

`Git <https://git-scm.com>`_ is a popular software tool that can be used to manage changes to code, including merging changes from multiple developers. Git organizes code into "repositories". On your machine, each repository corresponds to a directory (and all of its files and subdirectories).

`GitHub <https://github.com>`_ is a popular website for hosting Git repositories. In particular, GitHub facilities the merging of code changes among multiple developers. GitHub also makes it easy to distribute source code.

`Meld <http://meldmerge.org>`_ is a program for graphically displaying the differences between two text files. Meld is very helpful to understanding how files have been edited.

Installing and configurating the required software
--------------------------------------------------
This tutorial requires git and meld. Execute this command to install these package::

    apt-get install git meld libgnome-keyring-dev

Execute these commands to configure Git::

    git config --global user.name "John Doe"
    git config --global user.email "johndoe@example.com"

    cd /usr/share/doc/git/contrib/credential/gnome-keyring
    sudo make
    git config --global credential.helper /usr/share/doc/git/contrib/credential/gnome-keyring/git-credential-gnome-keyring

Add the following to ``~/.gitconfig``::

    [diff]
        tool = meld
    [difftool]
        prompt = false
    [difftool "meld"]
        cmd = meld "$LOCAL" "$REMOTE"

Instructions
------------------------------


Create a GitHub account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Visit `https://github.com <https://github.com>`_, click "Sign up", and follow the onscreen instructions.


Join the Karr Lab GitHub organization (group)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Send your GitHub username to Jonathan so he can add you to our group.


Create a repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#. Sign into GitHub
#. Add a repository at [https://github.com/new](https://github.com/new). Note, our convention is to use ``lower_camel_case`` package names.


Clone a repository (download it to your computer)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Git repositories are download from GitHub by "cloning" them. Execute the following command to clone the repository for these tutorials::

    git clone https://github.com/KarrLab/karr_lab_tutorials.git
    cd karr_lab_tutorials

This will create a directory with the name "karr_lab_tutorials", download all of the files for the repository from GitHub, and save them to the new directory.


Reviewing the files that have been changed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
After you have changed one or more files, you can see a list of the files that you have changed, added, or deleted by running ``git status``. To see the changes made to an individual file execute ``git difftool path/to/file``.


Commit changes to a repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
After you have changed one or more files, you can commit (save) those changes to the repository.

#. Select the changes that you would like to commit by executing ``git add path/to/file``. Repeat this for each change you would like to commit.
#. Execute ``git commit -m "<brief description of the changes>"``


Marking versions with tags
^^^^^^^^^^^^^^^^^^^^^^^^^^
You can use tags to mark the version numbers of key revisions. This can be done by running ``git tag <version_number>``.


Push your changes to GitHub
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Once you are ready to share one or more commits with the rest of our lab, you can push them to GitHub by executing ``git push``. If you also need to push tags, then you will need to run ``git push --tags``.


Pull changes from other developers from GitHub
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To retrieve changes made by other developers, execute ``git pull``. Note, if you have made changes which conflict with those made by other developes, Git will prompt you to manually review the conflict lines of code.


Using graphical programs to manage repositories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Several graphical programs are also available to manage Git repositories

* `Git Cola <https://git-cola.github.io/>`_
* `GitHub Desktop <https://desktop.github.com/>`_ (Windows, Mac)
* `GitKraken <https://www.gitkraken.com>`_
* `SmartGit <https://www.syntevo.com/smartgit/>`_


Additional Git tutorials
^^^^^^^^^^^^^^^^^^^^^^^^
There are numerous additional tutorials which cover more advanced concepts such as branching

* `Try Git <https://try.github.io>`_
* `Git tutorial <https://git-scm.com/docs/gittutorial>`_
* `Git Tutorials and Training <https://www.atlassian.com/git/tutorials>`_
