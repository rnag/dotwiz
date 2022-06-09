==========
Benchmarks
==========

The `benchmarks/`_ folder contains benchmark tests useful to compare
performance against similar libraries such as ``prodict``
and ``dotted-dict``.

Quickstart
----------

First, download the GitHub repo locally with ``git``:

.. code-block:: shell

    $ git clone https://github.com/rnag/dotwiz
    $ cd dotwiz

Ensure you have set up a `virtual environment`_ if you haven't already
done so.

Then, use ``make`` to install all benchmark and test dependencies:

.. code-block:: shell

    $ make init

Benchmarking
------------

Use ``pytest`` to benchmark the Python files in this directory.

For example, to benchmark the tests for retrieving keys (via "dot" attribute access):

.. code-block:: shell

    $ pytest benchmarks -m getattr --benchmark-compare

Pass the ``--benchmark-histogram`` argument to generate a histogram for a suite
of benchmark tests. For example:

.. code-block:: shell

    $ pytest benchmarks -m create --benchmark-histogram

To run all available benchmark tests:

.. code-block:: shell

    $ pytest benchmarks

Results
-------

Here are the benchmark results when running tests against other alternatives
or libraries.

:meth:`dataclasses.make_dataclass`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The results show that loading ``dict`` data via an approach with `make_dataclass`_ is
close to **100x** slower than an approach with a *dot-access* ``dict`` subclass such
as :class:`DotWiz`. Also see `my post on SO`_ for more info.

This is mainly because with a ``dict`` subclass, it doesn't need to dynamically generate a new class,
and scan through the dict object once to generate the dataclass fields and their types.

Though once the class is initially created, I was surprised to find that the dataclass approach performs about **5x**
better in an average case.

Creating a dot-access ``dict``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The results indicate it is about **5x** faster to *create* a :class:`DotWiz`
instance (from a ``dict`` object) as compared to other competitor libraries
such as ``dotsi`` and ``prodict`` - and up to **15x** faster than creating
a `Box`_.

Accessing keys by "dot" notation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The results show it is up to **10x** faster to *access* a key by dot
(or attribute) notation than with libraries such as ``prodict``, and
about **30x** faster than accessing keys from a `DotMap`_ for example.

.. _my post on SO: https://stackoverflow.com/a/72232461/10237506
.. _benchmarks/: https://github.com/rnag/dotwiz/tree/main/benchmarks
.. _virtual environment: https://realpython.com/python-virtual-environments-a-primer/
.. _make_dataclass: https://docs.python.org/3/library/dataclasses.html#dataclasses.make_dataclass
.. _Box: https://github.com/cdgriffith/Box/wiki/Quick-Start
.. _DotMap: https://pypi.org/project/dotmap
