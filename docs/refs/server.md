# SIDEX Server

The `sidex` package provides functions to launch a file server. A simple file sever is launched by calling `sidex.server` on a command line. The server process can be customized. Any pre- or post-processes can be appended to the server.


## Command-Line Tool

Basic usage of the command line tool provided by `sidex.server` is described.

``` console
$ python -m sidex.server -h
usage: server [-h] [--host host] [--port port] [--get-token token]
              [--put-token token] [--delete-token token] [--subdir subdir]
              [--debug]
              target

sidex server process

positional arguments:
  target                target directory

optional arguments:
  -h, --help            show this help message and exit
  --host host           set server hostname
  --port port           set server port number
  --get-token token     limit get function by setting token
  --put-token token     enable put function by setting token
  --delete-token token  enable delete function by setting token.
  --subdir subdir       set subdirectory
  --debug               enable debug messages
```
