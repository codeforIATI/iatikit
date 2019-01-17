class Validator(object):
    def __init__(self, is_valid, errors=None):
        if errors is not None:
            self._errors = errors
        else:
            self._errors = []
        self.is_valid = is_valid

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.is_valid)

    def __bool__(self):
        return self.is_valid

    @property
    def errors(self):
        return self._errors

    @property
    def error_summary(self):
        return [(x, 1) for x in self._errors]


class ValidationError(object):
    def __init__(self, msg, line=None, column=None, path=None):
        self.original_msg = msg
        self.line = line
        self.column = column
        self.path = path

        self.summary = msg
        self.details = ''

    def __repr__(self):
        max_length = 50
        txt = str(self)
        if len(txt) > max_length:
            txt = txt[:max_length-3] + '...'
        return '<{} ({})>'.format(self.__class__.__name__, txt)

    def __str__(self):
        return self.summary

    @property
    def url(self):
        return None

    @property
    def message(self):
        return str(self)
