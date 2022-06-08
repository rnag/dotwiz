=======
History
=======

0.3.0 (2022-06-08)
------------------

**Breaking Changes**

* Update the project classifier from *Production* to *Beta*, because the API is
  not yet stable, and future minor releases might introduce other breaking changes.
* ``dotwiz`` has officially dropped support for Python 3.6. This is due to a
  number of reasons, such as 3.6 reaching EOL some months back, and also
  libraries such as ``pyheck`` which only support Python 3.7+.
* Update the :meth:`__repr__` for :class:`DotWiz` to display a star character (✫)
  in place of the class name, just so it's a little easier to read.

**Features and Improvements**

* Add new :class:`DotWizPlus` class and implementation, which can be useful
  for special-cased keys like ``myTestKey`` and ``hello, world!``. This implementation
  mutates such keys to valid *snake case* identifier names, so the above key names
  would become ``my_test_key`` and ``hello_world``.
* Add new dependency on `pyheck`_.
* Refactor to pull out common or shared code into a :mod:`common` module.
* Update the docs and add a section on :class:`DotWizPlus`.
* Update theme for the docs, from ``alabaster`` to ``furo``.
* Update tests to maintain 100% code coverage.

.. _pyheck: https://kevinheavey.github.io/pyheck

0.2.0 (2022-06-05)
------------------

**Breaking Changes**

* Removed :class:`DotWiz` methods :meth:`from_dict` and :meth:`from_kwargs`,
  as these are now superseded by the :class:`DotWiz` constructor method.
* Update the signature of :func:`make_dot_wiz` to
  ``make_dot_wiz(*args, **kwargs)``

**Features and Improvements**

* It's now easier to create a :class:`DotWiz` object from a ``dict`` or from
  *keyword* arguments. The :meth:`__init__` constructor method can now directly
  be used instead.
* Add major performance improvements, so :class:`DotWiz` is now faster than ever.
* Add a :meth:`to_dict` method to enable a :class:`DotWiz` instance to be
  recursively converted back to a ``dict``.
* Refactor code to remove unnecessary stuff.
* Add GitHub badges and CI integration for `codecov`.
* Updated docs.

0.1.0 (2022-06-03)
------------------

* First release on PyPI.
