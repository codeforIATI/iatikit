from ..utils.exceptions import SchemaException
from ..utils.types import StringType


class ActivitySchema101:
    def __init__(self):
        self.version = '1.01'

    def iati_identifier(self):
        return StringType('iati-identifier/text()')

    def title(self):
        return StringType('title/text()')

    def description(self):
        return StringType('description/text()')


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
    raise SchemaException(msg)
