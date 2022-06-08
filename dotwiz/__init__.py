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
    'make_dot_wiz_plus'
]

from .main import DotWiz, make_dot_wiz
from .plus import DotWizPlus, make_dot_wiz_plus
