import mapbox_earcut as earcut
import numpy as np

verts = np.array([[0, 0], [1, 0], [1, 1]]).reshape(-1, 2)
rings = np.array([3])
print("v", np.shape(verts))
print("r", np.shape(rings))

for i in range(10000):
    result = earcut.triangulate_float32(verts, rings)

print(type(result))
print(result.dtype)
print(np.shape(result))
print(result)
print(verts)
print(verts[result])
