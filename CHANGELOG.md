# Changelog

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
