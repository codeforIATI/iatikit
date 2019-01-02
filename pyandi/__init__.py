from .data.registry import Registry
from .standard.codelist import CodelistSet
from .data.sector import Sector  # noqa: F401
from .utils import download  # noqa: F401
from .__version__ import __version__  # noqa: F401


def data(path=None):
    """Helper function for constructing a Registry object."""
    return Registry(path)


def codelists(path=None):
    """Helper function for fetching all codelists."""
    return CodelistSet(path)
