<div align="center">
  <img src=".github/assets/logo.png" height="128">
  <h1>
    Agentflow
  </h1>
  <h4>Agents, for Humans</h4>
</div>

<p align="center">
    <a href='https://github.com/achillesrasquinha/agentflow//actions?query=workflow:"Continuous Integration"'>
      <img src="https://img.shields.io/github/workflow/status/achillesrasquinha/agentflow/Continuous Integration?style=flat-square">
    </a>
    <a href="https://coveralls.io/github/achillesrasquinha/agentflow">
      <img src="https://img.shields.io/coveralls/github/achillesrasquinha/agentflow.svg?style=flat-square">
    </a>
    <a href="https://pypi.org/project/agentflow/">
      <img src="https://img.shields.io/pypi/v/agentflow.svg?style=flat-square">
    </a>
    <a href="https://pypi.org/project/agentflow/">
      <img src="https://img.shields.io/pypi/l/agentflow.svg?style=flat-square">
    </a>
    <a href="https://pypi.org/project/agentflow/">
		  <img src="https://img.shields.io/pypi/pyversions/agentflow.svg?style=flat-square">
	  </a>
    <a href="https://git.io/boilpy">
      <img src="https://img.shields.io/badge/made%20with-boilpy-red.svg?style=flat-square">
    </a>
</p>

### Table of Contents
* [Features](#features)
* [Quick Start](#quick-start)
* [Usage](#usage)
  * [Application Interface](#application-interface)
  * [Command-Line Interface](#command-line-interface)
* [FAQ](docs/faq.md)
* [License](#license)

### Features
* Python 2.7+ and Python 3.4+ compatible.

### Quick Start

```shell
$ pip install agentflow
```

Check out [installation](docs/source/install.rst) for more details.

### Usage

#### Application Interface

```python
>>> import agentflow
```


#### Command-Line Interface

```console
$ agentflow
Usage: agentflow [OPTIONS] COMMAND [ARGS]...

  Agentflow is a simple, yet powerful agentic framework, built for humans.

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  help     Show this message and exit.
  version  Show version and exit.
```


### Docker

Using `agentflow's` Docker Image can be done as follows:

```
$ docker run \
    --rm \
    -it \
    ghcr.io/achillesrasquinha/agentflow \
      --verbose
```

### License

This repository has been released under the [MIT License](LICENSE).

---

<div align="center">
  Made with ❤️ using <a href="https://git.io/boilpy">boilpy</a>.
</div>