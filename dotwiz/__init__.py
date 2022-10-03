"""
``dotwiz``
~~~~~~~~~~

DotWiz is a ``dict`` subclass that enables accessing (nested) keys
in dot notation.

Sample Usage::

    >>> from dotwiz import DotWiz
    >>> dw = DotWiz({'this': {'works': {'for': [{'nested': {'values': True}}]}}},
    ...             the_answer_to_life=42)
    >>> dw
    ✫(this=✫(works=✫(for=[✫(nested=✫(values=True))])), the_answer_to_life=42)
    >>> dw.this.works['for'][0].nested.values
    True
    >>> dw.the_answer_to_life
    42

For full documentation and more advanced usage, please see
<https://dotwiz.readthedocs.io>.

:copyright: (c) 2022 by Ritvik Nag.
:license: MIT, see LICENSE for more details.
"""

__all__ = [
    'DotWiz',
    'DotWizPlus',
    'make_dot_wiz',
    'make_dot_wiz_plus',
    'set_default_for_missing_keys',
]

from .main import DotWiz, make_dot_wiz
from .plus import DotWizPlus, make_dot_wiz_plus


def set_default_for_missing_keys(default=None,
                                 nested_access=False,
                                 overwrite=False):
    """
    Modifies :class:`DotWiz` and :class:`DotWizPlus` to add a custom
    :meth:`__getattr__`, so that accessing missing or non-existing attributes
    (keys) returns ``default`` instead of raising an :exc:`AttributeError`.

    This provides a handy alternative to the builtin :func:`hasattr`.

    For more details, see https://github.com/rnag/dotwiz/issues/14.

    Example::

        >>> from dotwiz import DotWiz, set_default_for_missing_keys
        >>> set_default_for_missing_keys('test')
        >>> dw = DotWiz(hello='world!')
        >>> assert dw.hello == 'world!'
        >>> assert dw.world == 'test'
        >>> set_default_for_missing_keys(nested_access=True, overwrite=True)
        >>> assert not dw.this.is_.a.nested.path

    :param default: The default value to return for missing or non-existing
      attributes (keys).
    :param nested_access: Enable nested dot access for missing keys in a
      path (without raising errors), such as `dw.hello.there.world`.
    :param overwrite: True to overwrite a class's `__getattr__()` method,
      if one already exists; defaults to False.

    """
    # enable nested dot access for missing keys in a path (if needed)
    if nested_access:
        from .frozen import FrozenDotWiz

        if default is not None:
            raise ValueError('cannot specify both default and nested_access')

        # create a frozen, global dot-dict object; this object can't
        # be modified or assigned to.
        default = FrozenDotWiz()

    for cls in DotWiz, DotWizPlus:
        cls_dict = cls.__dict__

        if not overwrite and '__getattr__' in cls_dict:
            msg = f'{cls.__qualname__} already defines a __getattr__() - ' \
                  f'pass `overwrite=True` to continue anyway.'
            raise ValueError(msg)

        def __getattr__(self: cls, item: str,
                        __default=default,
                        __get=cls_dict.get):

            return __get(item, __default)

        setattr(cls, '__getattr__', __getattr__)
