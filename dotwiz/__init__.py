"""
``dotwiz``
~~~~~~~~~~

A dict subclass that supports dot access notation

Sample Usage:

    >>> import dotwiz

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
