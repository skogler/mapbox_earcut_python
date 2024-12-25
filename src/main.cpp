#include "version.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <mapbox/earcut.hpp>

#include <iostream>
#include <vector>

#define IDENT_TO_STR(x) #x
#define MACRO_TO_STR(x) IDENT_TO_STR(x)

namespace py = pybind11;

//! vertices: (nverts, 2) numpy array
//! ring_end_indices: the end indices for each ring. The last value must be equal to the number of input vertices.
template<typename CoordT, typename IndexT>
py::array_t<IndexT> triangulate(py::array_t<CoordT> vertices, py::array_t<IndexT> ring_end_indices)
{
    if (vertices.ndim() != 2)
    {
        throw std::domain_error("The shape of vertices is not (nverts, 2)!");
    }
    if (ring_end_indices.ndim() != 1)
    {
        throw std::domain_error("ring_end_indices must be one-dimensional!");
    }
    auto v = vertices.unchecked();
    if (v.shape(1) != 2)
    {
        throw std::domain_error("The second dimension of vertices is not 2!");
    }
    auto r = ring_end_indices.template unchecked<1>();
    const auto num_rings = r.shape(0);
    const auto num_verts = v.shape(0);
    if (num_rings > 0)
    {
        if (r(num_rings - 1) != num_verts)
        {
             throw std::invalid_argument("The last value of ring_end_indices must be equal to the number of vertices!");
        }
    }
    else if (num_verts > 0)
    {
       throw std::invalid_argument("ring_end_indices is empty, but vertices is not! This seems like it might not be intentional.");
    }
    using Point = std::array<CoordT, 2>;
    std::vector<std::vector<Point>> polygon;
    for (int ring = 0; ring < r.shape(0); ++ring)
    {
        const int start = ring == 0 ? 0 : r(ring - 1);
        const int end = r(ring);
        if (end <= start)
        {
           throw std::invalid_argument("ring_end_indices must be in strictly increasing order!");
        }
        if (end > num_verts)
        {
           throw std::invalid_argument("ring_end_indices cannot contain values larger than the number of vertices!");
        }
        std::vector<Point> ring_verts;
        for (int idx = start; idx < end; ++idx)
        {
            ring_verts.push_back(Point{
                v(idx, 0),
                v(idx, 1)
            });
        }
        polygon.push_back(ring_verts);
    }

    std::vector<IndexT> indices = mapbox::earcut<IndexT>(polygon);

    return py::array(
        indices.size(),
        indices.data()
    );
}

PYBIND11_MODULE(mapbox_earcut, m)
{
    m.attr("__version__") = MACRO_TO_STR(VERSION_MAJOR) "." MACRO_TO_STR(VERSION_MINOR) "." MACRO_TO_STR(VERSION_PATCH);
    m.doc() = R"pbdoc(
        Python bindings to mapbox/earcut.hpp
        -----------------------

        .. currentmodule:: mapbox_earcut

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    m.def("triangulate_int32", &triangulate<int32_t, uint32_t>);
    m.def("triangulate_int64", &triangulate<int64_t, uint32_t>);
    m.def("triangulate_float32", &triangulate<float, uint32_t>);
    m.def("triangulate_float64", &triangulate<double, uint32_t>);
}
