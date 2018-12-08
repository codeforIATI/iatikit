class DateType:
    def __init__(self, version, datetype):
        self.datetype = datetype
        self._version = version

    def get(self):
        datetype = {
            'planned_start': ('start-planned', 1),
            'actual_start': ('start-actual', 2),
            'planned_end': ('end-planned', 3),
            'actual_end': ('end-actual', 4),
        }.get(self.datetype)
        if self._version.startswith('1'):
            datetype = datetype[0]
        else:
            datetype = datetype[1]
        return 'activity-date[@type="{}"]/@iso-date'.format(datetype)

    def where(self, op, value):
        op = {
            'lt': '<', 'lte': '<=',
            'gt': '>', 'gte': '>=',
            'eq': '=',
        }.get(op)
        if not op:
            raise Exception
        return 'number(translate({expr}, "-", "")) {op} {value}'.format(
            expr=self.get(),
            op=op,
            value=value.replace('-', ''),
        )


class StringType:
    def __init__(self, expr):
        self._expr = expr

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


class NarrativeType(StringType):
    def __init__(self, version, el):
        if version.startswith('1'):
            expr = '{}/text()'.format(el)
        else:
            expr = '{}/narrative/text()'.format(el)
        self._expr = expr

    def get(self):
        return self._expr
