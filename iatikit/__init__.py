from .standard.codelist import codelists  # noqa: F401
from .data.registry import Registry
from .data.publisher import Publisher  # noqa: F401
from .data.dataset import Dataset  # noqa: F401
from .data.activity import Activity  # noqa: F401
from .data.sector import Sector  # noqa: F401
from .utils import download  # noqa: F401
from .utils.config import CONFIG  # noqa: F401
from .__version__ import __version__  # noqa: F401


def data(path=None):
    """Helper function for constructing a Registry object."""
    return Registry(path)
