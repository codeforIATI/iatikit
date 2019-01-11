import requests


def get_iati_versions():
    versions_url = 'http://reference.iatistandard.org/201/codelists/' + \
                   'downloads/clv2/json/en/Version.json'
    versions = [d['code']
                for d in requests.get(versions_url).json()['data']]
    versions.reverse()
    return versions
