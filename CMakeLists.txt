cmake_minimum_required(VERSION 3.15...3.29)
project(mapbox_earcut LANGUAGES CXX)

if (NOT SKBUILD)
  message(WARNING "\
  This CMake file is meant to be executed using 'scikit-build-core'.
  Running it directly will almost certainly not produce the desired
  result. If you are a user trying to install this package, use the
  command below, which will install all necessary build dependencies,
  compile the package in an isolated environment, and then install it.
  =====================================================================
   $ uv sync
  =====================================================================
  If you are a software developer, and this is your own package, then
  it is usually much more efficient to install the build dependencies
  in your environment once and use the following command that avoids
  a costly creation of a new virtual environment at every compilation:
  =====================================================================
   $ uv build
  =====================================================================
  You may optionally add -Ceditable.rebuild=true to auto-rebuild when
  the package is imported. Otherwise, you need to rerun the above
  after editing C++ files.")
endif()

find_package(Python COMPONENTS Interpreter Development
        REQUIRED)
execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(
  _core
  # Target the stable ABI for Python 3.12+, which reduces
  # the number of binary wheels that must be built. This
  # does nothing on older Python versions
  STABLE_ABI
  FREE_THREADED
  NB_DOMAIN mapbox_earcut
  src/main.cpp
)
target_include_directories(_core PRIVATE include)

nanobind_add_stub(
  mapbox_earcut_stubs
  MODULE _core
  OUTPUT _core.pyi
  PYTHON_PATH $<TARGET_FILE_DIR:_core>
  DEPENDS _core
  MARKER_FILE py.typed
)

install(TARGETS _core LIBRARY DESTINATION mapbox_earcut)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/_core.pyi DESTINATION mapbox_earcut)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/py.typed DESTINATION mapbox_earcut)
install(FILES mapbox_earcut/__init__.py DESTINATION mapbox_earcut)
