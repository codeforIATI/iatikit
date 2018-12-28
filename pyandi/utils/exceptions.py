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
