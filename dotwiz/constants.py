"""
Project-specific constants
"""
import sys


# A two-element tuple containing the Python version, such as (3, 7)
__PY_VERSION__ = sys.version_info[:2]

# Methods for `dict`
__DICT_METHODS__ = frozenset(dir(dict) + ['__module__', '__slots__'])
