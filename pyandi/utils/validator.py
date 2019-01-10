class Validator(object):
    def __init__(self, is_valid, error_log=None):
        if error_log is not None:
            self.error_log = error_log
        else:
            self.error_log = []
        self.is_valid = is_valid

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.is_valid)

    def __bool__(self):
        return self.is_valid
