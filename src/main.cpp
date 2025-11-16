#include "version.hpp"

#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <mapbox/earcut.hpp>

#include <array>
#include <iostream>
#include <vector>

#define IDENT_TO_STR(x) #x
#define MACRO_TO_STR(x) IDENT_TO_STR(x)

namespace nb = nanobind ;

template<typename CoordT>
using VertexArray = nb::ndarray<CoordT, nb::shape<-1, 2>, nb::device::cpu>;

template<typename IndexT>
using IndexArray = nb::ndarray<IndexT, nb::shape<-1>, nb::device::cpu>;


//! vertices: (nverts, 2) numpy array
//! ring_end_indices: the end indices for each ring. The last value must be equal to the number of input vertices.
template<typename CoordT, typename IndexT>
auto triangulate(const VertexArray<CoordT>& vertices, const IndexArray<IndexT>& ring_end_indices)
{

    auto v = vertices;
    auto r = ring_end_indices;
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
    polygon.reserve(num_verts);
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
            ring_verts.push_back({v(idx, 0), v(idx, 1)});
        }
        polygon.push_back(ring_verts);
    }

    std::vector<IndexT> indices = mapbox::earcut<IndexT>(polygon);

    return nb::ndarray<IndexT, nb::numpy, nb::shape<-1>>(
        indices.data(),
        {indices.size()}
    ).cast();
}

NB_MODULE(_core, m)
{
    m.attr("__version__") = MACRO_TO_STR(VERSION_MAJOR) "." MACRO_TO_STR(VERSION_MINOR) "." MACRO_TO_STR(VERSION_PATCH);
    m.doc() = R"pbdoc(
        Python bindings to mapbox/earcut.hpp
        -----------------------

        .. currentmodule:: mapbox_earcut._core

        .. autosummary::
           :toctree: _generate

    )pbdoc";

    m.def("triangulate_int32", &triangulate<int32_t, uint32_t>);
    m.def("triangulate_int64", &triangulate<int64_t, uint32_t>);
    m.def("triangulate_float32", &triangulate<float, uint32_t>);
    m.def("triangulate_float64", &triangulate<double, uint32_t>);
}
