*********************************************************
Version and sharing data with Quilt
*********************************************************

Conducting modeling reproducibly and collaboratively requires versioning and sharing data. Although Git/GitHub is well suited to versioning and sharing code and models, Git/GitHub is not well-suited to data because Git is based on line-by-line differencing of text files, because Git is designed for small files under 100 MB, and because Git requires the entire package and its history to be cloned. `Quilt <https://quiltdata.com>`_ is a new system for versioning and sharing data with similar functionality to Git/GitHub and Docker/DockerHub. 


Overview
========

Quilt is based on versioning packages of data, which are hierarhical trees of directories and files.

Quilt provides the following features:

* Capability to version data packages
* Capability to share packages with collaborators and with the world
* Programmatic access to upload, download, and update packages
* Web pages with READMEs to view and browse packages, including their histories


Using Quilt
===========

First, create a Quilt account at `https://quiltdata.com/signup <https://quiltdata.com/signup>`_.

Second, run the following command to install Quilt::

    pip install quilt

Third, you can use the `install` command to install and upgrade Quilt packages. For example, run the following command to install the iris package from uciml::

    quilt install uciml/iris

Fourth, you can use the `inspect` command to view the contents of packages and you can use the `log` command to view the histories of packages. For example, run the following commands to inspect the iris package::

    quilt inspect uciml/iris
    quilt log uciml/iris

Fifth, you can use the `export` command to unpack packages to directories and files. For example, run the following command to unpack the iris package::

    quilt export uciml/iris /tmp/iris/

Sixth, you can use the `build` command to create packages from directories and the `version add` command to annotate the version of the created package. For example, run the following commands to build a new package containing the same iris data and annotate the version of the package::

    quilt build <username>/iris /tmp/iris/
    quilt version add <username>/iris 0.0.1 <hash>

Seventh, you can use the `push` command to upload packages to the Quilt server. For example, run the following commands to push the new package to the Quilt server. Optionally, you can use the `--public` flag to share the package with the world::

    quilt login
    quilt push --public <username>/iris/

In addition, Quilt provides the following utility commands:

* `quilt ls`: lists the packages installed on your system
* `quilt rm <owner>/<package>`: removes a package from your system
* `quilt delete <owner>/<package>`: removes a package from the Quilt server


Limitations and troubleshooting
===============================

Because Quilt is new, Quilt still has several quirks:

* Quilt automatically converts Excel files to CSV, losing all formatting.
* Node names cannot contain “.”.
* Only the package owner can push packages and create versions. Packages can't be authored collaboratively.
* Quilt doesn't support comments on revisions like Git
* The Quilt Python API prints results to stdout and doesn't return values.
* The Quilt user and package pages are rudimentary
* There is little documentation for Quilt
