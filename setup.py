import sys
import os
import subprocess
import re
import platform

import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

FILE_DIR = os.path.dirname(os.path.abspath(__file__))

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(
                re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
            '-DPYTHON_EXECUTABLE=' + sys.executable
        ]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += [
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(
                    cfg.upper(), extdir)
            ]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j8']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get('CXXFLAGS', ''), self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(
            ['cmake', ext.sourcedir] + cmake_args,
            cwd=self.build_temp,
            env=env)
        subprocess.check_call(
            ['cmake', '--build', '.'] + build_args, cwd=self.build_temp)


def get_readme_contents():
    with open(os.path.join(FILE_DIR, 'README.md'), 'r') as readme_file:
        return readme_file.read()


setup(
    name='mapbox_earcut',
    version='0.12.7',
    url='https://github.com/skogler/mapbox_earcut_python',
    author='Samuel Kogler',
    author_email='samuel.kogler@gmail.com',
    description=
    'Python bindings for the mapbox earcut C++ polygon triangulation library.',
    long_description=get_readme_contents(),
    long_description_content_type='text/markdown',
    license='ISC',
    ext_modules=[CMakeExtension('mapbox_earcut')],
    setup_requires=['setuptools_scm'],
    install_requires=['numpy'],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
    project_urls={
        'Source': 'https://github.com/skogler/mapbox_earcut_python',
        'Original C++ Source': 'https://github.com/mapbox/earcut.hpp',
    },
    include_package_data = True
)
