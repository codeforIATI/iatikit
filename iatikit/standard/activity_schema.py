from ..utils.exceptions import SchemaError
from ..utils.types import StringType, DateType, SectorType, XPathType, \
                          BooleanType
from ..utils.abstract import GenericType


# pylint: disable=too-many-ancestors
class ActivitySchema101(object):
    version = '1.01'

    @classmethod
    def xpath(cls):
        return XPathType('')

    @classmethod
    def id(cls):  # pylint: disable=invalid-name
        return cls.iati_identifier()

    @classmethod
    def iati_identifier(cls):
        return StringType('iati-identifier/text()')

    @classmethod
    def title(cls):
        return StringType('title/text()')

    @classmethod
    def description(cls):
        return StringType('description/text()')

    @classmethod
    def location(cls):
        return GenericType('location')

    @classmethod
    def sector(cls):
        # TODO: This should include lookups for other v1.0x vocabs
        condition = {
            '1': [None, 'DAC'],
            '2': 'DAC-3',
        }
        return SectorType('sector', condition)

    @classmethod
    def planned_start(cls):
        return DateType('activity-date[@type="start-planned"]/@iso-date')

    @classmethod
    def actual_start(cls):
        return DateType('activity-date[@type="start-actual"]/@iso-date')

    @classmethod
    def planned_end(cls):
        return DateType('activity-date[@type="end-planned"]/@iso-date')

    @classmethod
    def actual_end(cls):
        return DateType('activity-date[@type="end-actual"]/@iso-date')

    @classmethod
    def humanitarian(cls):
        return BooleanType('false')


class ActivitySchema102(ActivitySchema101):
    version = '1.02'


class ActivitySchema103(ActivitySchema102):
    version = '1.03'


class ActivitySchema104(ActivitySchema103):
    version = '1.04'


class ActivitySchema105(ActivitySchema104):
    version = '1.05'


class ActivitySchema201(ActivitySchema105):
    version = '2.01'

    @classmethod
    def title(cls):
        return StringType('title/narrative/text()')

    @classmethod
    def description(cls):
        return StringType('description/narrative/text()')

    @classmethod
    def sector(cls):
        condition = {
            '1': [None, '1'],
        }
        return SectorType('sector', condition)

    @classmethod
    def planned_start(cls):
        return DateType('activity-date[@type="1"]/@iso-date')

    @classmethod
    def actual_start(cls):
        return DateType('activity-date[@type="2"]/@iso-date')

    @classmethod
    def planned_end(cls):
        return DateType('activity-date[@type="3"]/@iso-date')

    @classmethod
    def actual_end(cls):
        return DateType('activity-date[@type="4"]/@iso-date')


class ActivitySchema202(ActivitySchema201):
    version = '2.02'

    @classmethod
    def humanitarian(cls):
        return BooleanType('@humanitarian')


class ActivitySchema203(ActivitySchema202):
    version = '2.03'


def get_activity_schema(version):
    schema = None

    if version == '2.03':
        schema = ActivitySchema203
    elif version == '2.02':
        schema = ActivitySchema202
    elif version == '2.01':
        schema = ActivitySchema201
    elif version == '1.05':
        schema = ActivitySchema105
    elif version == '1.04':
        schema = ActivitySchema104
    elif version == '1.03':
        schema = ActivitySchema103
    elif version == '1.02':
        schema = ActivitySchema102
    elif version == '1.01':
        schema = ActivitySchema101

    if not schema:
        msg = 'Unknown activity schema: version: {}'.format(version)
        raise SchemaError(msg)

    return schema
