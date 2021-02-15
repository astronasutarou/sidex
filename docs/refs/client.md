# SIDEX Client

Files under the `sidex` server can be accessed via HTTP. The `sidex.client` provides a command-line tool to make a request to the `sidex` server.

## Command-Line Tool

Basic usage of the command line tool provided by `sidex.client` is described as follows:

``` none
$ python -m sidex.client -h
usage: client [-h] [-d] [--token token] [filename] target

SIDEX minimal client

positional arguments:
  filename       filename to be uploaded (only requred in put mode)
  target         address to SIDEX server

optional arguments:
  -h, --help            show this help message and exit
  -d, --delete          delete file
  --token token         set token
```
