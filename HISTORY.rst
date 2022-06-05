=======
History
=======

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
