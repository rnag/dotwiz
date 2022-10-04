"""
Project-specific constant values.
"""
__all__ = [
    '__PY_VERSION__',
    '__PY_38_OR_ABOVE__',
    '__PY_39_OR_ABOVE__',
]

import sys


# Current system Python version
__PY_VERSION__ = sys.version_info[:2]

# Check if currently running Python 3.8 or higher
__PY_38_OR_ABOVE__ = __PY_VERSION__ >= (3, 8)

# Check if currently running Python 3.9 or higher
__PY_39_OR_ABOVE__ = __PY_VERSION__ >= (3, 9)
