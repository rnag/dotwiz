=======
Dot Wiz
=======

.. image:: https://img.shields.io/pypi/v/dotwiz.svg
        :target: https://pypi.org/project/dotwiz

.. image:: https://img.shields.io/pypi/pyversions/dotwiz.svg
        :target: https://pypi.org/project/dotwiz

.. image:: https://github.com/rnag/dotwiz/actions/workflows/dev.yml/badge.svg
        :target: https://github.com/rnag/dotwiz/actions/workflows/dev.yml

.. image:: https://readthedocs.org/projects/dotwiz/badge/?version=latest
        :target: https://dotwiz.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/rnag/dotwiz/shield.svg
     :target: https://pyup.io/repos/github/rnag/dotwiz/
     :alt: Updates


A `blazing fast`_ ``dict`` subclass that enables *dot access* notation via Python
attribute style. Nested ``dict`` and ``list`` values are automatically
transformed as well.

* Documentation: https://dotwiz.readthedocs.io.

Install
-------

.. code-block:: console

    $ pip install dotwiz

Usage
-----

Here is an example of how to create and use a ``DotWiz`` object:

.. code:: python3

    from dotwiz import DotWiz

    dw = DotWiz({'this': {'works': {'for': [{'nested': {'values': True}}]}}},
                the_answer_to_life=42)

    print(dw)
    # >  DotWiz(this=DotWiz(works=DotWiz(for=[DotWiz(nested=DotWiz(values=True))])),
    #           the_answer_to_life=42)

    assert dw.this.works['for'][0].nested.values  # True
    assert dw.the_answer_to_life == 42


Using ``make_dot_wiz`` allows you to pass in an iterable object when
creating a ``DotWiz`` object:

.. code:: python3

    from dotwiz import make_dot_wiz

    dw = make_dot_wiz([('hello, world!', 123), ('easy: as~ pie?', True)],
                      AnyKey='value')

    print(dw)
    #> DotWiz(AnyKey='value', hello, world!=123, easy: as~ pie?=True)

    assert dw['hello, world!'] == 123
    assert dw['easy: as~ pie?']
    assert dw.AnyKey == 'value'

Features
--------

* TODO

Benchmarks
----------

    The `benchmark`_ tests can be found in the project repo on GitHub.

Using a *dot-access* approach such as ``DotWiz`` can be up
to **100x** faster than with `make_dataclass`_ from the ``dataclasses`` module.

It's also about *5x* faster to create a ``DotWiz`` from a ``dict`` object
as compared to other libraries such as ``prodict`` -- or close to **15x** faster
than creating a `Box`_ -- and up to *10x* faster in general to access keys
by *dot* access -- or almost **30x** faster than accessing keys from a `DotMap`_!

Contributing
------------

Contributions are welcome! Open a pull request to fix a bug, or `open an issue`_
to discuss a new feature or change.

Check out the `Contributing`_ section in the docs for more info.

Credits
-------

This package was created with Cookiecutter_ and the `rnag/cookiecutter-pypackage`_ project template.

.. _blazing fast: https://dotwiz.readthedocs.io/en/latest/benchmarks.html#results
.. _Read The Docs: https://dotwiz.readthedocs.io
.. _Installation: https://dotwiz.readthedocs.io/en/latest/installation.html
.. _on PyPI: https://pypi.org/project/dotwiz/
.. _make_dataclass: https://docs.python.org/3/library/dataclasses.html#dataclasses.make_dataclass
.. _benchmark: https://github.com/rnag/dotwiz/tree/main/benchmarks
.. _Box: https://github.com/cdgriffith/Box/wiki/Quick-Start
.. _DotMap: https://pypi.org/project/dotmap
.. _`Contributing`: https://dotwiz.readthedocs.io/en/latest/contributing.html
.. _`open an issue`: https://github.com/rnag/dotwiz/issues
.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _`rnag/cookiecutter-pypackage`: https://github.com/rnag/cookiecutter-pypackage
