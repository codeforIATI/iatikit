from ..utils.abstract import GenericType


class StringType(GenericType):
    def where(self, op, value):
        if op in ['contains', 'startswith']:
            if op == 'startswith':
                op = 'starts-with'
            return '{expr}[{op}(., "{value}")]'.format(
                expr=self.get(),
                op=op,
                value=value,
            )
        return super().where(op, value)


class DateType(GenericType):
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
