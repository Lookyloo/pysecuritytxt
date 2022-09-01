# Python client and module for querying .well-known/security.txt files

Give it a domain, it tries to fetch the security.txt file

## Installation

```bash
pip install pysecuritytxt
```

## Usage

### Command line

You can use the `pysecuritytxt` command:

```bash
usage: pysecuritytxt [-h] [-p] url_or_domain

Try to get a security.txt file

positional arguments:
  url_or_domain  Try to get the file from there.

options:
  -h, --help     show this help message and exit
  -p, --parse    Parse the response, returns dict
```

### Library

See [API Reference](https://pysecuritytxt.readthedocs.io/en/latest/api_reference.html)
