"""
Dot Wiz
~~~~~~

A dict subclass that supports dot access notation

Sample Usage:

    >>> import dotwiz

For full documentation and more advanced usage, please see
<https://dotwiz.readthedocs.io>.

:copyright: (c) 2022 by Ritvik Nag.
:license:MIT, see LICENSE for more details.
"""

__all__ = [

]

import logging


# Set up logging to ``/dev/null`` like a library is supposed to.
# http://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger('dotwiz').addHandler(logging.NullHandler())
