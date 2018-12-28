# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.1] – 2018-12-28

### Added
- Log a warning when dataset XML is invalid
- Add some documentation in docs/ as well as some docstrings
- Be more specific about exception handling (i.e. don’t use `except:`)
- Add python 2.7 support
- Start adding tests; Setup travis and coveralls

### Changed
- Make `dataset.root` less strict
- metadata should return empty dict if file not found
- Simplify some set operations

## [1.5.0] – 2018-12-27

### Added
- Add a publisher metadata property
- Add `filter` as a synonym for `where`
- Add show() function to Publisher, Dataset and Activity models
- Add an `xpath` activity filter

### Changed
- `find` and `first` raise errors when no data found. `get` returns a default value
- `xml` property moved to `etree`; `raw_xml` property moved to `xml`

### Removed
- `get()` shouldn’t be a synonym for `all()`

## [1.4.0] – 2018-12-21

### Added
- Codelist support for all versions (i.e. v1.01+)
- Add `start` and `end` properties to activities
- Error when there’s no data ([#12](https://github.com/andylolz/pyandi/issues/12))
- Error when there are no codelists
- Improved sector support ([#22](https://github.com/andylolz/pyandi/pull/22))

### Changed
- Change internal representation of codelists
- Return python `date` objects for dates
- Always strip IATI identifiers

## [1.3.1] – 2018-12-17

### Fixed
- README render

## [1.3.0] – 2018-12-17

### Added
- Support set slicing
- Add a getter to all Sets. A set-getter!
- Ensure only known filters are used
- Allow for codelist filtering by code
- Add codelist `data` and `metadata` properties

### Changed
- Tidy up Activity model repr
- Reword examples in README slightly, for clarity
- Refactor activity property fetching, to be less clever
- Rename all exceptions, according to PEP8
- Major improvements to codelist code
- Always cast codelist codes to string

### Fixed
- Get date type exists filter working
- DateTypes should also be filterable by generic filters

### Removed
- Remove some cruft from the README about schema download

## [1.2.0] – 2018-12-10

### Added
- Add activity date filters

### Changed
- Add path to codelist functions

### Removed
- Remove schema download code
- Remove unused `xmlschema` package

## [1.1.1] – 2018-12-10

### Fixed
- Fix exception when there’s no existing data (bug in stale data warning)

## [1.1.0] – 2018-12-10

### Added
- `raw_xml` function added to dataset and activity
- Expand key-value extras in dataset metadata
- Add a filetype dataset filter
- Add a warning about stale data
- Add location, sector, title and description schema fields

### Changed
- Make it possible to download data to a custom path
- `is_valid` should just check for valid XML
- Determine filetype from metadata (instead of XML)
- Make `activity.dataset` public
- Use custom exceptions throughout

### Fixed
- Fix broken `@version` property
- Fix typo so metadata works again

## [1.0.0] – 2018-12-06

### Added
- Add functions to fetch all datasets and all activities

### Changed
- Move examples to README
- Standardise the set API with an abstract class
- Compute set size more efficiently
- Make API more consistent

## [0.2.0] – 2018-12-05

### Changed
- Remove download.metadata() (since metadata is now included in the data dump)
- Start using python logging
- Don’t parse XML until necessary
- Where path is useless – scrap it
- Scrap custom cache location

### Fixed
- Minor README updates

## [0.1.0] - 2018-12-04

### Added
- Initial release
