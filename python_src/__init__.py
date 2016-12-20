"""
This package is a small, fast implementation of an algorithm for
finding extremal rays of a polyhedral cone, with filtering.  It is
intended for finding normal surfaces in triangulated 3-manifolds, and
therefore does not implement various features that might be useful for
general extremal ray problems.
"""

from .FXraysmodule import find_Xrays

__version__ = '1.3.2'

def version():
    return __version__



