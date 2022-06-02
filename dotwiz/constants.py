"""
Project-specific constants
"""
import sys


# A two-element tuple containing the Python version, such as (3, 7)
_PY_VERSION = sys.version_info[:2]

# Methods for `dict`
_DICT_METHODS = frozenset(dir(dict) + ['__module__', '__slots__'])
