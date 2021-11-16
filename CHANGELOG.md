# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Change path to IATI data zip file

## [3.1.0] – 2021-10-05

### Fixed
- Include incomplete codelists in mapping file ([#54](https://github.com/codeforIATI/iatikit/issues/54))

### Changed
- Change path to IATI data zip file

## [3.0.3] – 2021-02-17

### Fixed
- raw_xml should return a byte string

## [3.0.1] – 2021-02-16

### Added
- Add Dataset.raw_xml

## [3.0.0] – 2021-02-15

### Fixed
- Fix bug so that PublisherSet deals with missing XML files. ([#52](https://github.com/codeforIATI/iatikit/issues/52))

### Changed
- Drop support for python 2.7

## [2.3.0] – 2020-12-16

### Changed
- Drop support for python 3.4 (again)
- Add support for python 3.8

## [2.2.12] – 2020-12-16

### Changed
- Unpin lxml requirement
- Update codelist download locations

## [2.2.11] – 2020-07-31

### Fixed
- Fix a longstanding python2.7 validator bug
- Fix a python 2.7 bug introduced in v2.2.10

## [2.2.10] – 2020-07-31

### Fixed
- Deal with missing XML files gracefully. ([#52](https://github.com/codeforIATI/iatikit/issues/52))

### Changed
- Don’t download metadata from gist (it’s now included in the IATI Data Dump zip file)

## [2.2.9] – 2019-11-09

### Changed
- Update URL for IATI data dump metadata (again)

## [2.2.8] – 2019-09-11

### Added
- Add a contributing guide

### Fixed
- Pin lxml, to maintain support for python 3.4

### Changed
- Update URL for IATI data dump metadata

## [2.2.7] – 2019-07-25

### Added
- Add a code of conduct

### Fixed
- Fix travis deployment for dot com
- Improve wording in installation docs

### Changed
- Change ownership of repo again

## [2.2.4] – 2019-05-19

### Added
- Added some Organisation tests
- Add support for python 3.4 and python 3.7

## [2.2.3] – 2019-05-18

### Fixed
- Don’t use the root logger. Instead, use iatikit’s own logger, and default to NullHandler. ([#46](https://github.com/codeforIATI/iatikit/issues/46))

## [2.2.2] – 2019-05-16

### Added
- API documentation for Organisation and OrganisationSet

### Fixed
- Make `dataset.root` return None if XML is invalid

## [2.2.1] – 2019-05-06

### Fixed
- Make multiple modifiers work ([#47](https://github.com/codeforIATI/iatikit/issues/47))

## [2.2.0] – 2019-05-06

### Added
- Added a dataset xpath filter

### Fixed
- Allow multiple filters of the same type to be specified ([#45](https://github.com/codeforIATI/iatikit/issues/45))
- Prevent looping twice when calling `all()` ([#44](https://github.com/codeforIATI/iatikit/issues/44))

### Removed
- Remove (experimental) fast identifier search

## [2.1.0] – 2019-04-21

### Changed
- Relax codelist item comparison ([#41](https://github.com/codeforIATI/iatikit/issues/41))

## [2.0.8] – 2019-04-20

### Added
- First pass at modelling IATI organisations ([#18](https://github.com/codeforIATI/iatikit/issues/18))

## [2.0.7] – 2019-04-20

### Added
- First pass at a `humanitarian` activity filter
- Add a `iatikit.download.standard()` command
- Add an optional `path` argument to `iatikit.data()`

## [2.0.6] – 2019-04-04

### Added
- Add some Windows installation instructions (tl;dr: use Jupyter)

### Fixed
- Deal with null paths
- Use `huge_tree` when parsing XML (to ensure big files still parse)

## [2.0.5] – 2019-03-12

### Fixed
- Fix "metadoota" typo!

## [2.0.4] – 2019-03-12

### Added
- (Re-)add metadata-only download

## [2.0.3] – 2019-03-12

### Fixed
- Fix dataset name filter

## [2.0.2] – 2019-03-12

### Changed
- Always use absolute paths to elements
- Refactor to better handle missing data

## [2.0.1] – 2019-02-27

### Added
- Add a dataset `schema` getter, and caching
- Add line number and path to codelist validation errors
- Add `dataset.unminify_xml()`, to ensure validation line numbers are meaningful
- Add activity-level schema validation
- Allow codelists to be filtered by name

### Changed
- `show()` uses dataset metadata
- Pretty print XML
- Rejig validation; make `dataset.version` fail on XML error
- Make `dataset.filetype` return None on failure

### Fixed
- Make XSD Schema constructor a bit more robust, and improve error handling
- Fix bug related to file and folder sort order
- Fix incorrect XSD error message regarding element ordering
- Allow datasets to be loaded from a StringIO
- Handle missing metadata in old codelists

## [2.0.0] – 2019-01-17

### Added
- Much better XSD and codelist validation messages

### Fixed
- Add checks to ensure filetype metadata from the registry is okay

### Changed
- Rename the project! "pyandi" -> "iatikit"

### Removed
- Drop `validate_unique_ids`. This should be part of ruleset validation

## [1.5.7] – 2019-01-15

### Added
- Add an IATI schema downloader
- Add IATI schema validation
- Add a fast find activity search ([#3](https://github.com/codeforIATI/iatikit/issues/3))
- Add `CodelistItem` and `Sector` comparison methods
- Add a `dataset.schema` method
- Make `download.codelists()` download codelist mappings, too
- Add a `CodelistMappings` class; Add codelist validation ([#31](https://github.com/codeforIATI/iatikit/issues/31))
- Add a `Validator` class, for storing the results of validation
- Remove `path` args from lots of constructors; use pyandi.ini instead ([#31](https://github.com/codeforIATI/iatikit/issues/31))

### Fixed
- Lots of pylint-related fixes
- Add missing _instance_class to `PublisherSet`
- Don’t patch `os.path.join` in tests ([#32](https://github.com/codeforIATI/iatikit/issues/32))

### Changed
- Don’t instantiate schemas – use static classes instead

### Removed
- Remove download helpers (they’re not really useful)

## [1.5.6] – 2019-01-08

### Added
- Add classifiers to setup

### Changed
- More import shuffling

### Fixed
- Fix pyversion badge
- Fix typo in docs

## [1.5.5] – 2019-01-08

### Changed
- Only declare requirements in setup
- Run tests with `python setup.py test`
- Run coverage by default when testing
- Shuffle imports about
- Remove support for python 3.4

## [1.5.4] – 2019-01-03

### Added
- Add a `__version__` string to the module (to help with debugging)
- Add badges to docs
- Use more custom exceptions
- Add lots more tests

### Fixed
- URL-encode d-portal param
- Ensure xml property returns a byte-string
- `where` should not modify the original set object

### Changed
- Split codelist attributes and metadata
- Rename codelist `name` filter to `slug`
- Make `codelist.complete` return a boolean

## [1.5.3] – 2019-01-02

### Added
- Various unit tests
- Make DateType filter accept a datetime.date
- Add `path` argument to Sector constructor
- Add a "Deployment" section to the README

### Changed
- Require unicodecsv

### Fixed
- Get tox working again

### Removed
- Comment out unused org-related code (temporarily)

## [1.5.2] – 2018-12-28

### Added
- Deploy to pypi from travis ([#26](https://github.com/codeforIATI/iatikit/issues/26))

### Changed
- Move repo from andylolz to pwyf

## [1.5.1] – 2018-12-28

### Added
- Log a warning when dataset XML is invalid
- Add some documentation in docs/ as well as some docstrings ([#16](https://github.com/codeforIATI/iatikit/issues/16))
- Be more specific about exception handling (i.e. don’t use `except:`)
- Add python 2.7 support
- Start adding tests; Setup travis and coveralls

### Changed
- Make `dataset.root` less strict
- metadata should return empty dict if file not found
- Simplify some set operations

## [1.5.0] – 2018-12-27

### Added
- Add a publisher metadata property ([#17](https://github.com/codeforIATI/iatikit/issues/17))
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
- Error when there’s no data ([#12](https://github.com/codeforIATI/iatikit/issues/12))
- Error when there are no codelists
- Improved sector support ([#22](https://github.com/codeforIATI/iatikit/pull/22))

### Changed
- Change internal representation of codelists ([#20](https://github.com/codeforIATI/iatikit/issues/20))
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
- Add a warning about stale data ([#8](https://github.com/codeforIATI/iatikit/issues/8))
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
