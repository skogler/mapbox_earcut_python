"""Type stubs for mapbox_earcut package."""

from mapbox_earcut._core import (
    __version__ as __version__,
    triangulate_float32 as triangulate_float32,
    triangulate_float64 as triangulate_float64,
    triangulate_int32 as triangulate_int32,
    triangulate_int64 as triangulate_int64,
)

__all__ = [
    "__version__",
    "triangulate_float32",
    "triangulate_float64",
    "triangulate_int32",
    "triangulate_int64",
]
