"""
Python bindings for the mapbox earcut C++ polygon triangulation library.

This module provides fast triangulation of 2D polygons using the Mapbox Earcut algorithm.
"""

# Import all functions from the compiled extension module
from ._core import (
    triangulate_float32,
    triangulate_float64,
    triangulate_int32,
    triangulate_int64,
    __version__,
)

__all__ = [
    "triangulate_float32",
    "triangulate_float64",
    "triangulate_int32",
    "triangulate_int64",
    "__version__",
]
