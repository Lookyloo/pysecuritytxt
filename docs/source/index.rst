.. PySecurityTXT documentation master file, created by
   sphinx-quickstart on Tue Mar 23 12:28:17 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PySecurityTXT's documentation!
=============================================

This is a module that (tries to) fetch the `security.txt file <https://securitytxt.org/>`  for a domain/url.

Installation
------------

The package is available on PyPi, so you can install it with::

  pip install pysecuritytxt


Usage
-----

You can use `pysecuritytxt` as a python script::

	$ pysecuritytxt -h
	usage: pysecuritytxt [-h] [-p] url_or_domain

	Try to get a security.txt file

	positional arguments:
	  url_or_domain  Try to get the file from there.

	options:
	  -h, --help     show this help message and exit
	  -p, --parse    Parse the response, returns dict



Or as a library:

.. toctree::
   :glob:

   api_reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
