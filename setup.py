from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

# TODO
VERSION = "1.0.2"

ext_modules = [
    Pybind11Extension(
        "mapbox_earcut",
        ["src/main.cpp"],
        include_dirs=["include"],
        define_macros=[("VERSION_INFO", VERSION)],
    ),
]

setup(
    ext_modules=ext_modules,
    cmdclass=dict(build_ext=build_ext),
)
