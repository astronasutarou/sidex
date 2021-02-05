# Simple Data Exchange Server over HTTP

The `sidex` provides a framework to host a minimal file server running on the `Flask`. Using the `sidex`, you can easily make your local file accessible on the network. The `sidex` server provides methods to fetch, upload, and delete files over HTTP.



## Install
The `sidex` is [available in the Python Package Index][pypi].

``` bash
pip install sidex
```


## Quick Start

Launching a server seems a good starting point to understand how the `sidex` works. The `sidex` provides a simple command-line functions to launch a server. The following command makes the files under the target directory available on the `localhost:8080`.

``` bash
python -m sidex.server path_to_target_directory
```

The `sidex` also provides a command-line function to make a request to the server. The file named `requested_file` under the target directory can be fetched by the following command.

``` bash
python -m sidex.client localhost:8080/requested_file
```

The fetched file is saved in the current directory.

Further information can be found in the following links:

- [Server](/server)
- [Client](/client)

## Dependencies
The `sidex` depends on the following modules:

- [`flask`][flask]: a lightweight WSGI web application framework.
- [`requests`][requests]: an elegant and simple HTTP library.


[pypi]: https://pypi.org/project/sidex/
[flask]: https://flask.palletsprojects.com/
[requests]: https://requests.readthedocs.io/
