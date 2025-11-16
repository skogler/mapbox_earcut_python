# Changelog

## 2.0.0

## Added

- Support for 3.14 and free-threaded Python

## Changed

- Wheels are now typed and have a minimal Python wrapper to contain the package in a directory when installed
- Wheels are now built using Python Stable ABI
- Due to conflicts with free-threaded Python had to remove support for Python Limited API
  - This just means new wheels will be required for every major Python version again
- Decided to bump the major version since the wheels won't be binary compatible
- Build now uses nanobind instead of pybind11

## [1.0.3]

## Changed

- Build now uses scikit-build instead of setuptools

## Added

- Wheels for Python 3.13

## [1.0.2]

## Changed

- Require Python 3.9
- Built wheels are now compatible with numpy 2
- Reduced set of pre-built wheels to match numpy
  - 32-bit Linux is not supported anymore:
    - numpy does not ship any wheels for these, so builds take a long time
    - numpy does not compile on some PyPy versions

## [1.0.1]

### Fixed

- Outdated `__version__` attribute

### Changed

- Update `earcut.hpp` to 2.2.4

### Added

- Build for Mac ARM (apple silicon)
- Build for Python 3.11 and 3.10

## [1.0.0]

### Changed

- Update `earcut.hpp` to 2.2.3 (with fixed includes, latest version from master).
- Change versioning scheme to enable semantic versioning independently from upstream versioning.

## [1.0.0]

### Changed

- Update `earcut.hpp` to 2.2.3 (with fixed includes, latest version from master).
- Change versioning scheme to enable semantic versioning independently from upstream versioning.

## [0.12.11] - 2021-11-04

### Fixed

- Out-of-bounds memory access on empty input (thanks @musicinmybrain).
- Missing import in earcut.hpp (thanks @Groctel).
- `__version__` attribute stringification.
