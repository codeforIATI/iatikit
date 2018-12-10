from ..utils.exceptions import SchemaException
from ..utils.types import StringType


class OrganisationSchema101:
    def __init__(self):
        self.version = '1.01'

    def org_identifier(self):
        return StringType('iati-identifier/text()', min=1, max=1)


class OrganisationSchema102(OrganisationSchema101):
    def __init__(self):
        self.version = '1.02'


class OrganisationSchema103(OrganisationSchema102):
    def __init__(self):
        self.version = '1.03'


class OrganisationSchema104(OrganisationSchema103):
    def __init__(self):
        self.version = '1.04'


class OrganisationSchema105(OrganisationSchema104):
    def __init__(self):
        self.version = '1.05'


class OrganisationSchema201(OrganisationSchema105):
    def __init__(self):
        self.version = '2.01'

    def org_identifier(self):
        return StringType('organisation-identifier/text()', min=1, max=1)


class OrganisationSchema202(OrganisationSchema201):
    def __init__(self):
        self.version = '2.02'


class OrganisationSchema203(OrganisationSchema202):
    def __init__(self):
        self.version = '2.03'


def get_organisation_schema(version):
    if version == '2.03':
        return OrganisationSchema203()
    elif version == '2.02':
        return OrganisationSchema202()
    elif version == '2.01':
        return OrganisationSchema201()
    elif version == '1.05':
        return OrganisationSchema105()
    elif version == '1.04':
        return OrganisationSchema104()
    elif version == '1.03':
        return OrganisationSchema103()
    elif version == '1.02':
        return OrganisationSchema102()
    elif version == '1.01':
        return OrganisationSchema101()

    msg = 'Unknown organisation schema: version: {}'.format(version)
    raise SchemaException(msg)
