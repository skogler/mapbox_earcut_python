import os

from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION = '1.0.1'

ext_modules = [
    Pybind11Extension('mapbox_earcut',
        ['src/main.cpp'],
        include_dirs=['include'],
        define_macros = [('VERSION_INFO', VERSION)],
        ),
]

def get_readme_contents():
    with open(os.path.join(FILE_DIR, 'README.md'), 'r') as readme_file:
        return readme_file.read()

setup(
    name='mapbox_earcut',
    version=VERSION,
    url='https://github.com/skogler/mapbox_earcut_python',
    author='Samuel Kogler',
    author_email='samuel.kogler@gmail.com',
    description=
    'Python bindings for the mapbox earcut C++ polygon triangulation library.',
    long_description=get_readme_contents(),
    long_description_content_type='text/markdown',
    license='ISC',
    ext_modules=ext_modules,
    install_requires=['numpy'],
    extras_require={'test': 'pytest'},
    cmdclass=dict(build_ext=build_ext),
    zip_safe=False,
    project_urls={
        'Source': 'https://github.com/skogler/mapbox_earcut_python',
        'Original C++ Source': 'https://github.com/mapbox/earcut.hpp',
    },
    include_package_data = True
)
