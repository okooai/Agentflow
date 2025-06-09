Agentflow: Agents, for Humans
=============================

Release v\ |version|. (:ref:`Installation <install>`)

.. image:: https://img.shields.io/coveralls/github/okooai/agentflow.svg?style=flat-square
    :target: https://coveralls.io/github/okooai/agentflow

.. image:: https://img.shields.io/pypi/pyversions/agentflow.svg?style=flat-square
    :target: https://pypi.org/project/agentflow/

.. .. image:: https://img.shields.io/docker/build/okooai/agentflow.svg?style=flat-square&logo=docker
..     :target: https://hub.docker.com/r/okooai/agentflow

.. image:: https://img.shields.io/badge/made%20with-boilpy-red.svg?style=flat-square
    :target: https://git.io/boilpy

.. image:: https://img.shields.io/badge/Say%20Thanks-🦉-1EAEDB.svg?style=flat-square
    :target: https://saythanks.io/to/achillesrasquinha

.. image:: https://img.shields.io/badge/donate-💵-f44336.svg?style=flat-square
    :target: https://paypal.me/achillesrasquinha

**Agentflow** is an asynchronous and security-first framework to build agentic workflows, designed to be simple, yet powerful.

**Behold, the power of Agentflow:**

.. code-block:: python

    >>> import agentflow as af

    >>> agent = af.hub("hello-world")
    >>> agent("Hello!")
    Hello! How can I help you today? 😊