cmake_minimum_required(VERSION 3.15...3.27)
project(mapbox_earcut LANGUAGES CXX)

if(CMAKE_VERSION VERSION_LESS 3.18)
  set(DEV_MODULE Development)
else()
  set(DEV_MODULE Development.Module)
endif()

find_package(Python COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)
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
