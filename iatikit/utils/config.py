from os.path import join

from configparser import ConfigParser


def _load_config():
    defaults = {
        'data_sources': {
            'url_containing_zip_url': 'https://iati-data-dump.codeforiati.org/download',
        },
        'paths': {
            'registry': join('__iatikitcache__', 'registry'),
            'standard': join('__iatikitcache__', 'standard'),
        },
        'github_api':{
            'access_token': "",
            'basic_auth_username': "",
            'basic_auth_password': ""
        }
    }
    config = ConfigParser()
    config.read_dict(defaults)
    config.read('iatikit.ini')
    return config


CONFIG = _load_config()
