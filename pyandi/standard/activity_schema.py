from ..utils.exceptions import SchemaError
from ..utils.types import StringType, DateType, SectorType
from ..utils.abstract import GenericType


class ActivitySchema101:
    def __init__(self):
        self.version = '1.01'

    def iati_identifier(self):
        return StringType('iati-identifier/text()')

    def title(self):
        return StringType('title/text()')

    def description(self):
        return StringType('description/text()')

    def location(self):
        return GenericType('location')

    def sector(self):
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
    if version == '2.03':
        return ActivitySchema203()
    elif version == '2.02':
        return ActivitySchema202()
    elif version == '2.01':
        return ActivitySchema201()
    elif version == '1.05':
        return ActivitySchema105()
    elif version == '1.04':
        return ActivitySchema104()
    elif version == '1.03':
        return ActivitySchema103()
    elif version == '1.02':
        return ActivitySchema102()
    elif version == '1.01':
        return ActivitySchema101()

    msg = 'Unknown activity schema: version: {}'.format(version)
    raise SchemaError(msg)
