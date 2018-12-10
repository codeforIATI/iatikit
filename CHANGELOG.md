# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
