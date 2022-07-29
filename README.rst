=======
Dot Wiz
=======

.. image:: https://img.shields.io/pypi/v/dotwiz.svg
        :target: https://pypi.org/project/dotwiz

.. image:: https://img.shields.io/pypi/pyversions/dotwiz.svg
        :target: https://pypi.org/project/dotwiz

.. image:: https://codecov.io/gh/rnag/dotwiz/branch/main/graph/badge.svg?token=J3YW230U8Z
        :target: https://codecov.io/gh/rnag/dotwiz

.. image:: https://github.com/rnag/dotwiz/actions/workflows/dev.yml/badge.svg
        :target: https://github.com/rnag/dotwiz/actions/workflows/dev.yml

.. image:: https://pyup.io/repos/github/rnag/dotwiz/shield.svg
        :target: https://pyup.io/repos/github/rnag/dotwiz/
        :alt: Updates


A `blazing fast`_ ``dict`` wrapper that enables *dot access* notation via Python
attribute style. Nested ``dict`` and ``list`` values are automatically
transformed as well.

* Documentation: https://dotwiz.readthedocs.io.

-------------------

Assume you have a simple ``dict`` object, with dynamic keys::

    >>> my_dict = {'this': {'dict': {'has': [{'nested': {'data': True}}]}}}

If the goal is to access a nested value, you could do it like this::

    >>> my_dict['this']['dict']['has'][0]['nested']['data']
    True

Or, using ``DotWiz``::

    >>> from dotwiz import DotWiz
    >>> dw = DotWiz(my_dict)
    >>> dw.this.dict.has[0].nested.data
    True

**Note**: This library can also make inaccessible keys safe -- check out `an example`_ with ``DotWizPlus``.

.. _an example: https://dotwiz.readthedocs.io/en/latest/usage.html#dotwizplus

Install
-------

.. code-block:: console

    $ pip install dotwiz

Usage
-----

``DotWiz``
~~~~~~~~~~

Here is an example of how to create and use a ``DotWiz`` object:

.. code:: python3

    from dotwiz import DotWiz

    dw = DotWiz({'this': {'works': {'for': [{'nested': {'values': True}}]}}},
                the_answer_to_life=42)

    print(dw)
    # >  ✫(this=✫(works=✫(for=[✫(nested=✫(values=True))])),
    #      the_answer_to_life=42)

    assert dw.this.works['for'][0].nested.values  # True
    assert dw.the_answer_to_life == 42

    print(dw.to_dict())
    # >  {'this': {'works': {'for': [{'nested': {'values': True}}]}},
    #     'the_answer_to_life': 42}

Using ``make_dot_wiz`` allows you to pass in an iterable object when
creating a ``DotWiz`` object:

.. code:: python3

    from dotwiz import make_dot_wiz

    dw = make_dot_wiz([('hello, world!', 123), ('easy: as~ pie?', True)],
                      AnyKey='value')

    print(dw)
    #> ✫(AnyKey='value', hello, world!=123, easy: as~ pie?=True)

    assert dw['hello, world!'] == 123
    assert dw['easy: as~ pie?']
    assert dw.AnyKey == 'value'

    print(dw.to_json())
    #> {"AnyKey": "value", "hello, world!": 123, "easy: as~ pie?": true}

``DotWizPlus``
~~~~~~~~~~~~~~

``DotWiz+`` enables you to turn special-cased keys, such as names with spaces,
into valid *snake_case* words in Python, as shown below. Also see the note
on `Issues with Invalid Characters`_ below.

.. code:: python3

    from dotwiz import DotWizPlus

    my_dict = {'THIS': {'1': {'is': [{'For': {'AllOf': {'My !@ Fans!': True}}}]}}}
    dw = DotWizPlus(my_dict)

    print(dw)
    # >  ✪(this=✪(_1=✪(is_=[✪(for_=✪(all_of=✪(my_fans=True)))])))

    # True
    assert dw.this._1.is_[0].for_.all_of.my_fans

    # alternatively, you can access it like a dict with the original keys:
    assert dw['THIS']['1']['is'][0]['For']['AllOf']['My !@ Fans!']

    print(dw.to_dict())
    # >  {'THIS': {'1': {'is': [{'For': {'AllOf': {'My !@ Fans!': True}}}]}}}

    print(dw.to_attr_dict())
    # >  {'this': {'_1': {'is_': [{'for_': {'all_of': {'my_fans': True}}}]}}

    print(dw.to_json(snake=True))
    # >  {"this": {"1": {"is": [{"for": {"all_of": {"my_fans": true}}}]}}}

Issues with Invalid Characters
******************************

A key name in the scope of the ``DotWizPlus`` implementation must be:

* a valid, *lower-* and *snake-* cased `identifier`_ in python.
* not a reserved *keyword*, such as ``for`` or ``class``.
* not override ``dict`` method declarations, such as ``items``, ``get``, or ``values``.

In the case where your key name does not conform, the library will mutate
your key to a safe, snake-cased format.

Spaces and invalid characters are replaced with ``_``. In the case
of a key beginning with an *int*, a leading ``_`` is added.
In the case of a *keyword* or a ``dict`` method name, a trailing
``_`` is added. Keys that appear in different cases, such
as ``myKey`` or ``My-Key``, will all be converted to
a *snake case* variant, ``my_key`` in this example.

Finally, check out `this example`_ which brings home all
that was discussed above.

Features
--------

* TODO

Benchmarks
----------

    Check out the `Benchmarks`_ section in the docs for more info.

Using a *dot-access* approach such as ``DotWiz`` can be up
to **100x** faster than with `make_dataclass`_ from the ``dataclasses`` module.

It's also about *5x* faster to create a ``DotWiz`` from a ``dict`` object
as compared to other libraries such as ``prodict`` -- or close to **15x** faster
than creating a `Box`_ -- and up to *10x* faster in general to access keys
by *dot* notation -- or almost **30x** faster than accessing keys from a `DotMap`_.

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
.. _Issues with Invalid Characters: https://dotwiz.readthedocs.io/en/latest/#issues-with-invalid-characters
.. _identifier: https://www.askpython.com/python/python-identifiers-rules-best-practices
.. _this example: https://dotwiz.readthedocs.io/en/latest/usage.html#complete-example
.. _make_dataclass: https://docs.python.org/3/library/dataclasses.html#dataclasses.make_dataclass
.. _Benchmarks: https://dotwiz.readthedocs.io/en/latest/benchmarks.html
.. _Box: https://github.com/cdgriffith/Box/wiki/Quick-Start
.. _DotMap: https://pypi.org/project/dotmap
.. _`Contributing`: https://dotwiz.readthedocs.io/en/latest/contributing.html
.. _`open an issue`: https://github.com/rnag/dotwiz/issues
.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _`rnag/cookiecutter-pypackage`: https://github.com/rnag/cookiecutter-pypackage
