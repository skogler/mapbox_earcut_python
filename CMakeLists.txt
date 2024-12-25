cmake_minimum_required(VERSION 3.15...3.29)
project(mapbox_earcut LANGUAGES CXX)

set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(mapbox_earcut src/main.cpp)
target_include_directories(mapbox_earcut PRIVATE include)
install(TARGETS mapbox_earcut DESTINATION .)