from configparser import ConfigParser
from os import getenv
from os.path import join


def _load_config():
    defaults = {
        "data_sources": {
            "zip_url": getenv("IATIKIT_CONFIG_DATASOURCES_ZIP_URL", ""),
        },
        "paths": {
            "registry": join("__iatikitcache__", "registry"),
            "standard": join("__iatikitcache__", "standard"),
        },
    }
    config = ConfigParser()
    config.read_dict(defaults)
    config.read("iatikit.ini")
    return config


CONFIG = _load_config()
