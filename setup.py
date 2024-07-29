import os

from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext


def _get_version() -> str:
    """
    Get the version defined in `pyproject.toml` to prevent
    requiring the version to be specified in two places.

    Note that Python only introduced a TOML parser in
    Python 3.11 so this requires `pip install tomli` for older
    versions of Python.
    """
    try:
        # we could also do this with
        # if `sys.version_info >= (3, 11)`
        from tomllib import load
    except BaseException:
        # a parser with the same API from pypi
        from tomli import load

    # current working directory
    cwd = os.path.abspath(os.path.expanduser(os.path.dirname(__file__)))
    # file-relative pyproject path
    path = os.path.join(cwd, "pyproject.toml")
    with open(path, "rb") as f:
        pyproject = load(f)

    return pyproject["project"]["version"]


ext_modules = [
    Pybind11Extension(
        "earcutx",
        ["src/main.cpp"],
        include_dirs=["include"],
        define_macros=[("VERSION_INFO", _get_version())],
    ),
]

setup(
    ext_modules=ext_modules,
    cmdclass=dict(build_ext=build_ext),
)
