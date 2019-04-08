import logging
from datetime import datetime

from ..data.sector import Sector
from ..standard.codelist import CodelistSet, CodelistItem
from ..utils.abstract import GenericType


class StringType(GenericType):
    def where(self, operation, value):
        if operation in ['contains', 'startswith']:
            if operation == 'startswith':
                operation = 'starts-with'
            return '{expr}[{operation}(., "{value}")]'.format(
                expr=self.get(),
                operation=operation,
                value=value,
            )
        return super(StringType, self).where(operation, value)


class DateType(GenericType):
    def where(self, operation, value):
        operator = {
            'lt': '<', 'lte': '<=',
            'gt': '>', 'gte': '>=',
            'eq': '=',
        }.get(operation)
        if operator:
            tmpl = 'number(translate({expr}, "-", "")) {operator} {value}'
            return tmpl.format(
                expr=self.get(),
                operator=operator,
                value=str(value).replace('-', ''),
            )
        return super(DateType, self).where(operation, value)

    def run(self, etree):
        dates = []
        dates_str = etree.xpath(self.get())
        for date_str in dates_str:
            try:
                dates.append(datetime.strptime(date_str, '%Y-%m-%d').date())
            except ValueError:
                logging.warning('Invalid date: "%s"', date_str)
        return dates


class SectorType(GenericType):
    def __init__(self, expr, condition):
        super(SectorType, self).__init__(expr)
        self.condition = condition

    @staticmethod
    def _vocab_condition(conditions):
        conditions_list = []
        if not isinstance(conditions, list):
            conditions = [conditions]
        for condition in conditions:
            if condition is None:
                conditions_list.append('not(@vocabulary)')
            else:
                conditions_list.append('@vocabulary = "{}"'.format(condition))
        conditions_str = ' or '.join(conditions_list)
        if len(conditions_list) > 1:
            conditions_str = '({})'.format(conditions_str)
        return conditions_str

    def where(self, operation, value):
        if operation == 'in':
            if not isinstance(value, Sector) or value.vocabulary.code != '2':
                raise Exception('{} is not a sector category'.format(value))
            codelist_items = CodelistSet().get('Sector').where(
                category=value.code.code).all()
            conditions = ' or '.join(['@code = "{code}"'.format(code=c.code)
                                      for c in codelist_items])
            conditions = ['(' + conditions + ')']
            conditions.append(
                self._vocab_condition(self.condition.get('1')))
            return '{expr}[{conditions}]'.format(
                expr=self.get(),
                conditions=' and '.join(conditions),
            )
        elif operation == 'eq':
            conditions = []
            if not isinstance(value, Sector):
                raise Exception('{} is not a sector'.format(value))
            if isinstance(value.code, CodelistItem):
                code = value.code.code
            else:
                code = value.code
            if code is not None:
                conditions.append('@code = "{code}"'.format(code=code))
            if value.vocabulary is not None:
                conds = self.condition.get(value.vocabulary.code,
                                           value.vocabulary.code)
                conditions.append(self._vocab_condition(conds))
            return '{expr}[{conditions}]'.format(
                expr=self.get(),
                conditions=' and '.join(conditions),
            )
        return super(SectorType, self).where(operation, value)

    def run(self, etree):
        return [Sector(x.get('code'),
                       vocabulary=x.get('vocabulary', '1'),
                       percentage=x.get('percentage'))
                for x in etree.xpath(self.get())]


class XPathType(GenericType):
    def where(self, operation, value):
        return value


class BooleanType(GenericType):
    def run(self, etree):
        return etree.xpath('{expr} = "true" or {expr} = "1"'.format(
            expr=self.get(),
        ))

    def where(self, operation, value):
        if value is not bool(value):
            raise Exception('{} is not a boolean'.format(value))
        if value:
            return '{expr} = "true" or {expr} = "1"'.format(
                expr=self.get(),
            )
        else:
            return 'not({expr}) or {expr} = "false" or {expr} = "0"'.format(
                expr=self.get(),
            )
