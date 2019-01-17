class SchemaError(Exception):
    """Raised when an unknown schema is requested."""
    pass


class FilterError(Exception):
    """Raised when an unknown or invalid set filter is used."""
    pass


class NoDataError(Exception):
    """Raised when no data is found in the local cache."""
    pass


class NoCodelistsError(Exception):
    """Raised when no codelists are found in the local cache."""
    pass


class UnknownSectorVocabError(Exception):
    """Raised when a sector vocabulary is used that is not on the
       IATI codelists.
    """
    pass


class UnknownSectorCodeError(Exception):
    """Raised when a sector code is used that is not on the
       IATI codelists.
    """
    pass


class InvalidSectorCodeError(Exception):
    """Raised when a sector is constructed using a non-sector codelist item
    """
    pass


class SchemaNotFoundError(Exception):
    pass


class MappingsNotFoundError(Exception):
    pass
