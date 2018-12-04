class ActivitySchema:
    def __init__(self, version):
        self._version = version

    def get_query(self, shortcut, operator=None, value=None):
        # TODO
        res = self.getattr(shortcut)

    @property
    def title(self):
        if self._version.startswith('1'):
            xpath = 'title/text()'
        else:
            xpath = 'title/narrative/text()'
        return {
            'xpath': xpath,
            'type': StringType,
        }

    @property
    def description(self):
        if self._version.startswith('1'):
            xpath = 'description/text()'
        else:
            xpath = 'description/narrative/text()'
        return {
            'xpath': xpath,
            'type': StringType,
        }


class StringType:
    pass
