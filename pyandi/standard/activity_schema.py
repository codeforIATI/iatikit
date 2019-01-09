from ..utils.exceptions import SchemaError
from ..utils.types import StringType, DateType, SectorType, XPathType
from ..utils.abstract import GenericType


class ActivitySchema101(object):
    def __init__(self):
        self.version = '1.01'

    def xpath(self):
        return XPathType('')

    def id(self):  # pylint: disable=invalid-name
        return self.iati_identifier()

    def iati_identifier(self):
        return StringType('iati-identifier/text()')

    def title(self):
        return StringType('title/text()')

    def description(self):
        return StringType('description/text()')

    def location(self):
        return GenericType('location')

    def sector(self):
        # TODO: This should include lookups for other v1.0x vocabs
        condition = {
            '1': [None, 'DAC'],
            '2': 'DAC-3',
        }
        return SectorType('sector', self.version, condition)

    def planned_start(self):
        return DateType('activity-date[@type="start-planned"]/@iso-date')

    def actual_start(self):
        return DateType('activity-date[@type="start-actual"]/@iso-date')

    def planned_end(self):
        return DateType('activity-date[@type="end-planned"]/@iso-date')

    def actual_end(self):
        return DateType('activity-date[@type="end-actual"]/@iso-date')


class ActivitySchema102(ActivitySchema101):
    def __init__(self):
        self.version = '1.02'


class ActivitySchema103(ActivitySchema102):
    def __init__(self):
        self.version = '1.03'


class ActivitySchema104(ActivitySchema103):
    def __init__(self):
        self.version = '1.04'


class ActivitySchema105(ActivitySchema104):
    def __init__(self):
        self.version = '1.05'


class ActivitySchema201(ActivitySchema105):
    def __init__(self):
        self.version = '2.01'

    def title(self):
        return StringType('title/narrative/text()')

    def description(self):
        return StringType('description/narrative/text()')

    def sector(self):
        condition = {
            '1': [None, '1'],
        }
        return SectorType('sector', self.version, condition)

    def planned_start(self):
        return DateType('activity-date[@type="1"]/@iso-date')

    def actual_start(self):
        return DateType('activity-date[@type="2"]/@iso-date')

    def planned_end(self):
        return DateType('activity-date[@type="3"]/@iso-date')

    def actual_end(self):
        return DateType('activity-date[@type="4"]/@iso-date')


class ActivitySchema202(ActivitySchema201):
    def __init__(self):
        self.version = '2.02'


class ActivitySchema203(ActivitySchema202):
    def __init__(self):
        self.version = '2.03'


def get_activity_schema(version):
    schema = None

    if version == '2.03':
        schema = ActivitySchema203()
    elif version == '2.02':
        schema = ActivitySchema202()
    elif version == '2.01':
        schema = ActivitySchema201()
    elif version == '1.05':
        schema = ActivitySchema105()
    elif version == '1.04':
        schema = ActivitySchema104()
    elif version == '1.03':
        schema = ActivitySchema103()
    elif version == '1.02':
        schema = ActivitySchema102()
    elif version == '1.01':
        schema = ActivitySchema101()

    if not schema:
        msg = 'Unknown activity schema: version: {}'.format(version)
        raise SchemaError(msg)

    return schema
