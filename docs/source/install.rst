.. _install:

### Installation

#### Installation via pip

The recommended way to install **agentflow** is via `pip`.

```shell
$ pip install agentflow
```

For instructions on installing python and pip see “The Hitchhiker’s Guide to Python” 
[Installation Guides](https://docs.python-guide.org/starting/installation/).

#### Building from source

`agentflow` is actively developed on [https://github.com](https://github.com/achillesrasquinha/agentflow)
and is always avaliable.

You can clone the base repository with git as follows:

```shell
$ git clone https://github.com/achillesrasquinha/agentflow
```

Optionally, you could download the tarball or zipball as follows:

##### For Linux Users

```shell
$ curl -OL https://github.com/achillesrasquinha/tarball/agentflow
```

##### For Windows Users

```shell
$ curl -OL https://github.com/achillesrasquinha/zipball/agentflow
```

Install necessary dependencies

```shell
$ cd agentflow
$ pip install -r requirements.txt
```

Then, go ahead and install agentflow in your site-packages as follows:

```shell
$ python setup.py install
```

Check to see if you’ve installed agentflow correctly.

```shell
$ agentflow --help
```