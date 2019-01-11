from os.path import join

from configparser import ConfigParser


def _load_config():
    defaults = {
        'paths': {
            'registry': join('__pyandicache__', 'registry'),
            'standard': join('__pyandicache__', 'standard'),
        }
    }
    config = ConfigParser()
    config.read_dict(defaults)
    config.read('pyandi.ini')
    return config


CONFIG = _load_config()
