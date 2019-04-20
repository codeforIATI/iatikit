from .activity_schema import get_activity_schema
from .organisation_schema import get_organisation_schema


def get_schema(filetype, version):
    if filetype == 'activity':
        return get_activity_schema(version)
    elif filetype == 'organisation':
        return get_organisation_schema(version)
