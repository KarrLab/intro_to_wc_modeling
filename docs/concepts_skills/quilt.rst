*********************************************************
Version and sharing data with Quilt
*********************************************************

Conducting modeling reproducibly and collaboratively requires versioning and sharing data. Although Git/GitHub is well suited to versioning and sharing code and models, Git/GitHub is not well-suited to data because Git is based on line-by-line differencing of text files, because Git is designed for small files under 100 MB, and because Git requires the entire package and its history to be cloned. `Quilt <https://open.quiltdata.com>`_ is a new system for versioning and sharing data with similar functionality to Git/GitHub and Docker/DockerHub. 


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

See the `Quilt documentation <https://docs.quiltdata.com/>`_.
