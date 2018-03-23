cmake_minimum_required(VERSION 3.10)
project(mapbox_earcut)

add_subdirectory(pybind11)
    
pybind11_add_module(mapbox_earcut src/main.cpp)
target_include_directories(mapbox_earcut PUBLIC include)
set_property(TARGET mapbox_earcut PROPERTY CXX_STANDARD 14)