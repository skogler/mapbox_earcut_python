cmake_minimum_required(VERSION 3.15...3.29)
project(mapbox_earcut LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development
        REQUIRED)
execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(
  mapbox_earcut
  src/main.cpp
)
target_include_directories(mapbox_earcut PRIVATE include)
install(TARGETS mapbox_earcut DESTINATION .)
