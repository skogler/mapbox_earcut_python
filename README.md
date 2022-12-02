# mapbox_earcut

[![PyPi version](https://badgen.net/pypi/v/mapbox-earcut/)](https://pypi.org/project/mapbox-earcut)

Python bindings for the C++ implementation of the Mapbox Earcut library, which
provides very fast and quite robust triangulation of 2D polygons.

Original code: [earcut.hpp](https://github.com/mapbox/earcut.hpp)

Original description:

> The library implements a modified ear slicing algorithm, optimized by
> [z-order curve](http://en.wikipedia.org/wiki/Z-order_curve) hashing and
> extended to handle holes, twisted polygons, degeneracies and self-intersections
> in a way that doesn't _guarantee_ correctness of triangulation, but attempts to
> always produce acceptable results for practical data like geographical shapes.

Provided functions (depending on dtype of vertex data):
```python
triangulate_float32
triangulate_float64
triangulate_int32
triangulate_int64
```

Example:
```python

import mapbox_earcut as earcut
import numpy as np

# A Nx2 array of vertices. Must be 2D.
verts = np.array([[0, 0], [1, 0], [1, 1]]).reshape(-1, 2)

# An array of end-indices for each ring.
# The first ring is the outer contour of the polygon.
# Subsequent ones are holes.
# This implies that the last index must always be equal to the size of verts!
rings = np.array([3])

result = earcut.triangulate_float32(verts, rings)

# Result is an np.ndarray with dtype np.uint32 and shape (3,)
# containing indices into the verts array.

print(verts[result])
# [[1 0]
#  [1 1]
#  [0 0]]
```
