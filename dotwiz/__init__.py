"""
``dotwiz``
~~~~~~~~~~

DotWiz is a ``dict`` subclass that enables accessing (nested) keys
in dot notation.

Sample Usage:

    >>> from dotwiz import DotWiz
    >>> dw = DotWiz({'this': {'works': {'for': [{'nested': 'values'}]}}})
    >>> dw
    DotWiz(this=DotWiz(works=DotWiz(for=[DotWiz(nested='values')])))
    >>> dw.this.works['for'][0].nested
    'values'

For full documentation and more advanced usage, please see
<https://dotwiz.readthedocs.io>.

:copyright: (c) 2022 by Ritvik Nag.
:license:MIT, see LICENSE for more details.
"""

__all__ = [
    'DotWiz',
    'make_dot_wiz'
]

from .main import DotWiz, make_dot_wiz
