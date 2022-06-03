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


A ``dict`` subclass that is easy to create, and supports *fast* dot access notation.

* Documentation: https://dotwiz.readthedocs.io.

Installation
------------

The Dot Wiz library is available `on PyPI`_, and can be installed with ``pip``:

.. code-block:: shell

    $ pip install dotwiz

The ``dotwiz`` library officially supports **Python 3.6** or higher.

Usage
-----

Here is an example using :meth:`DotWiz.from_dict` to create a :class:`DotWiz`
object from a ``dict`` object:

.. code:: python3

    from dotwiz import DotWiz

    dw = DotWiz.from_dict({'this': {'works': {'for': [{'nested': 'values'}]}}})

    print(dw)
    #>  DotWiz(this=DotWiz(works=DotWiz(for=[DotWiz(nested='values')])))

    assert dw.this.works['for'][0].nested == 'values'  # True

Using :func:`make_dot_wiz` allows you to pass in keyword arguments when
creating a :class:`DotWiz` object:

    Note: This helper function is also aliased to :meth:`DotWiz.from_kwargs`.

.. code:: python3

    from dotwiz import make_dot_wiz

    dw = make_dot_wiz({'hello, world!': 123}, AnyKey='value', isActive=True)

    assert dw['hello, world!'] == 123
    assert dw.AnyKey == 'value'
    assert dw.isActive

Features
--------

* TODO

Contributing
------------

Contributions are welcome! Open a pull request to fix a bug, or `open an issue`_
to discuss a new feature or change.

Check out the `Contributing`_ section in the docs for more info.

Credits
-------

This package was created with Cookiecutter_ and the `rnag/cookiecutter-pypackage`_ project template.

.. _Read The Docs: https://dotwiz.readthedocs.io
.. _Installation: https://dotwiz.readthedocs.io/en/latest/installation.html
.. _on PyPI: https://pypi.org/project/dotwiz/
.. _`Contributing`: https://dotwiz.readthedocs.io/en/latest/contributing.html
.. _`open an issue`: https://github.com/rnag/dotwiz/issues
.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _`rnag/cookiecutter-pypackage`: https://github.com/rnag/cookiecutter-pypackage
