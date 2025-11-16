"""
Thread safety tests for free-threaded Python (PEP 703).

These tests validate that the mapbox_earcut library is safe to use
with multiple threads when running Python with the GIL disabled.
"""

import sys
from concurrent.futures import ThreadPoolExecutor
import threading
from typing import Any, Callable, List, Optional, Tuple, Union

import mapbox_earcut as earcut
import numpy as np
from numpy.typing import NDArray
import pytest


def run_threaded(
    func: Callable[..., Any],
    num_threads: int = 8,
    pass_count: bool = False,
    pass_barrier: bool = False,
    outer_iterations: int = 1,
    prepare_args: Optional[Callable[[], List[Any]]] = None,
) -> None:
    """
    Runs a function many times in parallel.

    This helper is adapted from NumPy's testing utilities and is designed
    to expose race conditions and thread safety issues.

    Args:
        func: The function to run in parallel
        num_threads: Number of threads to spawn
        pass_count: If True, pass thread index as first argument to func
        pass_barrier: If True, pass a threading.Barrier as argument to func
        outer_iterations: Number of times to repeat the entire test
        prepare_args: Optional function that returns a list of arguments
    """
    for _ in range(outer_iterations):
        with ThreadPoolExecutor(max_workers=num_threads) as tpe:
            if prepare_args is None:
                args = []
            else:
                args = prepare_args()
            if pass_barrier:
                barrier = threading.Barrier(num_threads)
                args.append(barrier)
            else:
                barrier = None
            if pass_count:
                all_args = [(func, i, *args) for i in range(num_threads)]
            else:
                all_args = [(func, *args) for i in range(num_threads)]

            futures = []
            try:
                for arg in all_args:
                    futures.append(tpe.submit(*arg))
            finally:
                if len(futures) < num_threads and barrier is not None:
                    barrier.abort()
            for f in futures:
                f.result()


# Basic thread safety tests


def test_parallel_triangulate_float32_simple() -> None:
    """Test that multiple threads can triangulate simple polygons simultaneously."""
    results: List[Optional[NDArray[np.uint32]]] = [None] * 8

    def closure(i: int, b: threading.Barrier) -> None:
        # Create per-thread data to avoid sharing arrays
        verts = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.float32).reshape(-1, 2)
        rings = np.array([3])

        # Synchronize all threads to maximize chance of race condition
        _ = b.wait()

        # Perform triangulation
        result = earcut.triangulate_float32(verts, rings)

        # Store result
        results[i] = result

    run_threaded(closure, num_threads=8, pass_barrier=True, pass_count=True)

    # Verify all threads got correct results
    expected = np.array([1, 2, 0])
    for i, result in enumerate(results):
        assert result is not None, f"Thread {i} didn't produce a result"
        assert result.dtype == np.uint32
        assert result.shape == (3,)
        assert np.array_equal(result, expected), f"Thread {i} got incorrect result"


def test_parallel_triangulate_float64_simple() -> None:
    """Test that multiple threads can triangulate with float64 simultaneously."""
    results: List[Optional[NDArray[np.uint32]]] = [None] * 8

    def closure(i: int, b: threading.Barrier) -> None:
        verts = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.float64).reshape(-1, 2)
        rings = np.array([3])
        _ = b.wait()
        result = earcut.triangulate_float64(verts, rings)
        results[i] = result

    run_threaded(closure, num_threads=8, pass_barrier=True, pass_count=True)

    expected = np.array([1, 2, 0])
    for result in results:
        assert result is not None
        assert np.array_equal(result, expected)


def test_parallel_triangulate_int32_simple() -> None:
    """Test that multiple threads can triangulate with int32 simultaneously."""
    results: List[Optional[NDArray[np.uint32]]] = [None] * 8

    def closure(i: int, b: threading.Barrier) -> None:
        verts = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.int32).reshape(-1, 2)
        rings = np.array([3])
        _ = b.wait()
        result = earcut.triangulate_int32(verts, rings)
        results[i] = result

    run_threaded(closure, num_threads=8, pass_barrier=True, pass_count=True)

    expected = np.array([1, 2, 0])
    for result in results:
        assert result is not None
        assert np.array_equal(result, expected)


def test_parallel_triangulate_int64_simple() -> None:
    """Test that multiple threads can triangulate with int64 simultaneously."""
    results: List[Optional[NDArray[np.uint32]]] = [None] * 8

    def closure(i: int, b: threading.Barrier) -> None:
        verts = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.int64).reshape(-1, 2)
        rings = np.array([3])
        _ = b.wait()
        result = earcut.triangulate_int64(verts, rings)
        results[i] = result

    run_threaded(closure, num_threads=8, pass_barrier=True, pass_count=True)

    expected = np.array([1, 2, 0])
    for result in results:
        assert result is not None
        assert np.array_equal(result, expected)


# Complex polygon thread safety tests


def test_parallel_triangulate_square() -> None:
    """Test parallel triangulation of a square."""
    results: List[Optional[NDArray[np.uint32]]] = [None] * 16

    def closure(i: int, b: threading.Barrier) -> None:
        # Square polygon
        verts = np.array(
            [[0, 0], [10, 0], [10, 10], [0, 10]], dtype=np.float32
        ).reshape(-1, 2)
        rings = np.array([4])

        _ = b.wait()
        result = earcut.triangulate_float32(verts, rings)
        results[i] = result

    run_threaded(
        closure, num_threads=16, pass_barrier=True, pass_count=True, outer_iterations=3
    )

    # All results should have 6 indices (2 triangles)
    for result in results:
        assert result is not None
        assert result.dtype == np.uint32
        assert result.shape == (6,)


def test_parallel_triangulate_with_hole() -> None:
    """Test parallel triangulation of a polygon with a hole."""
    results: List[Optional[NDArray[np.uint32]]] = [None] * 8

    def closure(i: int, b: threading.Barrier) -> None:
        # Outer square
        outer = np.array([[0, 0], [10, 0], [10, 10], [0, 10]], dtype=np.float32)

        # Inner square (hole)
        inner = np.array([[2, 2], [8, 2], [8, 8], [2, 8]], dtype=np.float32)

        verts = np.vstack([outer, inner]).reshape(-1, 2)
        rings = np.array([4, 8])  # First ring ends at 4, second at 8

        _ = b.wait()
        result = earcut.triangulate_float32(verts, rings)
        results[i] = result

    run_threaded(closure, num_threads=8, pass_barrier=True, pass_count=True)

    # All results should be consistent
    first_result = results[0]
    assert first_result is not None
    for result in results[1:]:
        assert result is not None
        assert result.shape == first_result.shape
        assert np.array_equal(result, first_result)


def test_parallel_triangulate_complex_shape() -> None:
    """Test parallel triangulation with a more complex polygon."""
    results: List[Optional[NDArray[np.uint32]]] = [None] * 12

    def closure(i: int, b: threading.Barrier) -> None:
        # Hexagon
        angles = np.linspace(0, 2 * np.pi, 7)[:-1]  # 6 points
        verts = np.column_stack([np.cos(angles), np.sin(angles)]).astype(np.float64)
        rings = np.array([6])

        _ = b.wait()
        result = earcut.triangulate_float64(verts, rings)
        results[i] = result

    run_threaded(
        closure, num_threads=12, pass_barrier=True, pass_count=True, outer_iterations=2
    )

    # Hexagon should produce 12 indices (4 triangles)
    for result in results:
        assert result is not None
        assert result.shape == (12,)


# Stress tests


def test_high_contention_same_shape() -> None:
    """
    Stress test with many threads processing the same shape.

    This test runs many threads all triangulating the same geometry
    to maximize the chance of exposing race conditions.
    """
    num_threads = 32
    results: List[Optional[NDArray[np.uint32]]] = [None] * num_threads

    def closure(i: int, b: threading.Barrier) -> None:
        verts = np.array([[0, 0], [5, 0], [5, 5], [0, 5]], dtype=np.float32).reshape(
            -1, 2
        )
        rings = np.array([4])

        _ = b.wait()
        result = None
        # Run multiple times in each thread
        for _ in range(10):
            result = earcut.triangulate_float32(verts, rings)
        results[i] = result

    run_threaded(
        closure,
        num_threads=num_threads,
        pass_barrier=True,
        pass_count=True,
        outer_iterations=5,
    )

    # Verify all results are consistent
    for result in results:
        assert result is not None
        assert result.shape == (6,)


def test_mixed_operations() -> None:
    """Test mixing different data types in parallel."""
    results: List[Optional[NDArray[np.uint32]]] = [None] * 16

    def closure(i: int, b: threading.Barrier) -> None:
        # Each thread uses a different dtype based on its index
        dtypes = [np.float32, np.float64, np.int32, np.int64]
        funcs: List[Callable[[Any, Any], NDArray[np.uint32]]] = [
            earcut.triangulate_float32,
            earcut.triangulate_float64,
            earcut.triangulate_int32,
            earcut.triangulate_int64,
        ]

        dtype = dtypes[i % 4]
        func = funcs[i % 4]

        verts = np.array([[0, 0], [1, 0], [1, 1]], dtype=dtype).reshape(-1, 2)
        rings = np.array([3])

        _ = b.wait()
        result = func(verts, rings)
        results[i] = result

    run_threaded(
        closure, num_threads=16, pass_barrier=True, pass_count=True, outer_iterations=10
    )

    expected = np.array([1, 2, 0])
    for result in results:
        assert result is not None
        assert np.array_equal(result, expected)


def test_varying_sizes() -> None:
    """Test with varying polygon sizes across threads."""
    results: List[Optional[NDArray[np.uint32]]] = [None] * 20

    def closure(i: int, b: threading.Barrier) -> None:
        # Create polygons of different sizes based on thread index
        num_sides = 3 + (i % 8)  # 3 to 10 sides
        angles = np.linspace(0, 2 * np.pi, num_sides + 1)[:-1]
        verts = np.column_stack([np.cos(angles), np.sin(angles)]).astype(np.float32)
        rings = np.array([num_sides])

        _ = b.wait()
        result = earcut.triangulate_float32(verts, rings)
        results[i] = result

    run_threaded(
        closure, num_threads=20, pass_barrier=True, pass_count=True, outer_iterations=3
    )

    # Verify results exist and have reasonable sizes
    for i, result in enumerate(results):
        assert result is not None
        num_sides = 3 + (i % 8)
        # n-sided polygon should produce (n-2) triangles = (n-2)*3 indices
        expected_indices = (num_sides - 2) * 3
        assert result.shape == (expected_indices,), (
            f"Thread {i}: {num_sides}-sided polygon should produce {expected_indices} indices"
        )


# Error handling thread safety tests


def test_parallel_invalid_rings() -> None:
    """Test that multiple threads can handle invalid input simultaneously."""
    exceptions: List[Optional[ValueError]] = [None] * 8

    def closure(i: int, b: threading.Barrier) -> None:
        verts = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.float32).reshape(-1, 2)
        rings = np.array([5])  # Invalid: larger than verts

        _ = b.wait()
        try:
            _ = earcut.triangulate_float32(verts, rings)
            exceptions[i] = None
        except ValueError as e:
            exceptions[i] = e

    run_threaded(closure, num_threads=8, pass_barrier=True, pass_count=True)

    # All threads should have raised ValueError
    for i, exc in enumerate(exceptions):
        assert exc is not None, f"Thread {i} should have raised ValueError"
        assert isinstance(exc, ValueError)


def test_parallel_mixed_valid_invalid() -> None:
    """Test mixing valid and invalid inputs across threads."""
    results: List[Optional[Tuple[str, Union[NDArray[np.uint32], ValueError]]]] = [
        None
    ] * 16

    def closure(i: int, b: threading.Barrier) -> None:
        verts = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.float32).reshape(-1, 2)

        # Even threads: valid input, Odd threads: invalid input
        if i % 2 == 0:
            rings = np.array([3])
        else:
            rings = np.array([5])  # Invalid

        _ = b.wait()
        try:
            result = earcut.triangulate_float32(verts, rings)
            results[i] = ("success", result)
        except ValueError as e:
            results[i] = ("error", e)

    run_threaded(
        closure, num_threads=16, pass_barrier=True, pass_count=True, outer_iterations=5
    )

    # Verify results match expectations
    for i, result in enumerate(results):
        assert result is not None
        status, value = result
        if i % 2 == 0:
            assert status == "success", f"Thread {i} should have succeeded"
            assert isinstance(value, np.ndarray)
            assert value.shape == (3,)
        else:
            assert status == "error", f"Thread {i} should have raised error"
            assert isinstance(value, ValueError)


# Helper functions


def is_free_threaded() -> bool:
    """Check if Python is running with free-threading enabled."""
    return getattr(sys, "_is_gil_enabled", lambda: True)() is False


pytestmark = pytest.mark.skipif(
    not is_free_threaded(),
    reason="Thread safety tests are most relevant for free-threaded Python",
)
