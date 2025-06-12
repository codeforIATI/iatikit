import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

http_adapter = HTTPAdapter(max_retries=Retry(total=3))


def get_iati_versions():
    session = requests.Session()
    session.mount('https://', http_adapter)
    versions_url = 'http://reference.iatistandard.org/201/codelists/' + \
                   'downloads/clv2/json/en/Version.json'
    versions_response = session.get(versions_url)
    versions_response.raise_for_status()
    versions = [
        d['code']
        for d in versions_response.json()['data']
    ]
    versions.reverse()
    return versions
