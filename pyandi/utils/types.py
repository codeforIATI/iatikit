class StringType:
    def __init__(self, expr, **kwargs):
        self._expr = expr
        # TODO: kwargs

    def get(self):
        return self._expr

    def where(self, op, value):
        if op in ['contains', 'startswith']:
            if op == 'startswith':
                op = 'starts-with'
            return '{expr}[{op}(., "{value}")]'.format(
                expr=self.get(),
                op=op,
                value=value,
            )
        elif op == 'exists':
            if value is False:
                subop = '= 0'
            else:
                subop = '!= 0'
            return 'count({expr}) {subop}'.format(
                expr=self.get(),
                subop=subop,
            )
        elif op == 'eq':
            return '{expr} = "{value}"'.format(
                expr=self.get(),
                value=value,
            )
        raise Exception
