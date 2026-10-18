import mapbox_earcut as earcut
import numpy as np
import pytest


def test_valid_triangulation_float32():
    verts = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.float32).reshape(-1, 2)
    rings = np.array([3])

    result = earcut.triangulate_float32(verts, rings)

    assert result.dtype == np.uint32
    assert result.shape == (3,)
    assert np.array_equal(result, np.array([1, 2, 0]))


def test_valid_triangulation_float64():
    verts = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.float64).reshape(-1, 2)
    rings = np.array([3])

    result = earcut.triangulate_float64(verts, rings)

    assert result.dtype == np.uint32
    assert result.shape == (3,)
    assert np.array_equal(result, np.array([1, 2, 0]))


def test_valid_triangulation_int32():
    verts = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.int32).reshape(-1, 2)
    rings = np.array([3])

    result = earcut.triangulate_int32(verts, rings)

    assert result.dtype == np.uint32
    assert result.shape == (3,)
    assert np.array_equal(result, np.array([1, 2, 0]))


def test_valid_triangulation_int64():
    verts = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.int64).reshape(-1, 2)
    rings = np.array([3])

    result = earcut.triangulate_int64(verts, rings)

    assert result.dtype == np.uint32
    assert result.shape == (3,)
    assert np.array_equal(result, np.array([1, 2, 0]))


def test_inverted_vertex_order():
    verts = np.array(list(reversed([[0, 0], [1, 0], [1, 1]])), dtype=np.int32).reshape(
        -1, 2
    )
    rings = np.array([3])

    result = earcut.triangulate_int32(verts, rings)

    assert result.dtype == np.uint32
    assert result.shape == (3,)
    assert np.array_equal(result, np.array([1, 0, 2]))


def test_no_triangles():
    verts = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.int32).reshape(-1, 2)
    rings = np.array([2, 3])

    result = earcut.triangulate_int32(verts, rings)

    assert result.dtype == np.uint32
    assert result.shape == (0,)


def test_end_index_too_large():
    verts = np.array([[0, 0], [1, 0], [1, 1]]).reshape(-1, 2)
    rings = np.array([5])

    with pytest.raises(ValueError):
        _ = earcut.triangulate_float32(verts, rings)


def test_end_index_too_small():
    verts = np.array([[0, 0], [1, 0], [1, 1]]).reshape(-1, 2)
    rings = np.array([2])

    with pytest.raises(ValueError):
        _ = earcut.triangulate_float32(verts, rings)


def test_end_index_neg():
    verts = np.array([[0, 0], [1, 0], [1, 1]]).reshape(-1, 2)
    rings = np.array([-1])

    with pytest.raises(ValueError):
        _ = earcut.triangulate_float32(verts, rings)


def test_rings_not_increasing():
    verts = np.array([[0, 0], [1, 0], [1, 1]]).reshape(-1, 2)
    rings = np.array([3, 0, 3])

    with pytest.raises(ValueError):
        _ = earcut.triangulate_float32(verts, rings)


def test_rings_same():
    verts = np.array([[0, 0], [1, 0], [1, 1]]).reshape(-1, 2)
    rings = np.array([3, 3])

    with pytest.raises(ValueError):
        _ = earcut.triangulate_float32(verts, rings)


def test_no_rings():
    verts = np.array([[0, 0], [1, 0], [1, 1]]).reshape(-1, 2)
    rings = np.array([])

    with pytest.raises(ValueError):
        _ = earcut.triangulate_float32(verts, rings)


def test_empty_data():
    verts = np.array([]).reshape(-1, 2)
    rings = np.array([])

    result = earcut.triangulate_float32(verts, rings)

    assert result.shape == (0,)


@pytest.mark.parametrize("dtype", ["int32", "int64", "float32", "float64"])
@pytest.mark.parametrize("readonly_vertices, readonly_rings", [
    (True, False), (False, True), (True, True),
])
def test_readonly_inputs(dtype, readonly_vertices, readonly_rings):
    vertices = np.array([[0, 0], [4, 0], [4, 3]], dtype=dtype)
    rings = np.array([3], dtype=np.uint32)
    original_vertices = vertices.copy()
    original_rings = rings.copy()
    if readonly_vertices:
        vertices.flags.writeable = False
    if readonly_rings:
        rings.flags.writeable = False

    result = getattr(earcut, "triangulate_" + dtype)(vertices, rings)

    assert result.dtype == np.uint32
    np.testing.assert_array_equal(result, [1, 2, 0])
    np.testing.assert_array_equal(vertices, original_vertices)
    np.testing.assert_array_equal(rings, original_rings)
    assert vertices.flags.writeable == (not readonly_vertices)
    assert rings.flags.writeable == (not readonly_rings)
