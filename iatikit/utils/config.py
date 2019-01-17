from os.path import join

from configparser import ConfigParser


def _load_config():
    defaults = {
        'paths': {
            'registry': join('__iatikitcache__', 'registry'),
            'standard': join('__iatikitcache__', 'standard'),
        }
    }
    config = ConfigParser()
    config.read_dict(defaults)
    config.read('iatikit.ini')
    return config


CONFIG = _load_config()
