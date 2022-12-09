# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2022-12-18
### Added
- `grid.op` methods for collecting cells using an `operator` comparison (keep collecting while `operator.gt(seed_cell.value, next_cell.value)` is true)

## [0.1.1] - 2021-12-12
### Added
- `__version__` being dynamically pulled from package metadata
- Get test coverage up to 100%

## [0.1.0] - 2021-12-11
### Added
- Basic functionality for Grid, Collection, and Cell objects
- Examples - two advent of code puzzles, one project euler puzzle
- Tests
- Early documentation
