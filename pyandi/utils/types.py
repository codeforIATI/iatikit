from ..utils.abstract import GenericType
from datetime import datetime


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
        operator = {
            'lt': '<', 'lte': '<=',
            'gt': '>', 'gte': '>=',
            'eq': '=',
        }.get(op)
        if operator:
            return 'number(translate({expr}, "-", "")) {op} {value}'.format(
                expr=self.get(),
                op=operator,
                value=value.replace('-', ''),
            )
        return super().where(op, value)

    def exec(self, xml):
        dates = []
        dates_str = xml.xpath(self.get())
        for date_str in dates_str:
            try:
                dates.append(datetime.strptime(date_str, '%Y-%m-%d').date())
            except ValueError:
                # TODO: Add a warning here
                pass
        return dates
