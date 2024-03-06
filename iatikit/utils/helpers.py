import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

http_adapter = HTTPAdapter(max_retries=Retry(total=3))


def get_iati_versions():
    session = requests.Session()
    session.mount('https://', http_adapter)
    versions_url = 'http://reference.iatistandard.org/201/codelists/' + \
                   'downloads/clv2/json/en/Version.json'
    versions = [
        d['code']
        for d in session.get(versions_url).json()['data']
    ]
    versions.reverse()
    return versions
