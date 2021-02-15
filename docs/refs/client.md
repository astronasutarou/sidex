# SIDEX Client

Files under the `sidex` server can be accessed via HTTP. The `sidex.client` provides a command-line tool to make a request to the `sidex` server.

## Command-Line Tool

Basic usage of the command line tool provided by `sidex.client` is described as follows:

``` none
$ python -m sidex.client -h
usage: client [-h] [-d] [-f filename] [--token token] url

SIDEX minimal client

positional arguments:
  url                   address to SIDEX server

optional arguments:
  -h, --help            show this help message and exit
  -d, --delete          delete file
  -f filename, --file filename
                        file to be upload
  --token token         set token
```
