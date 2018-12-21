import logging
from datetime import datetime

from ..data.sector import Sector
from ..standard.codelist import CodelistSet, CodelistItem
from ..utils.abstract import GenericType


logger = logging.getLogger(__name__)


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
                logger.warn('Invalid date: "{}"'.format(date_str))
        return dates


class SectorType(GenericType):
    def __init__(self, expr, version, condition):
        super().__init__(expr)
        self.condition = condition

    def _vocab_condition(self, conditions):
        conditions_list = []
        for condition in conditions:
            if condition is None:
                conditions_list.append('not(@vocabulary)')
            else:
                conditions_list.append('@vocabulary = "{}"'.format(condition))
        conditions_str = ' or '.join(conditions_list)
        if len(conditions_list) > 1:
            conditions_str = '({})'.format(conditions_str)
        return conditions_str

    def where(self, op, value):
        if op == 'in':
            if type(value) is not Sector or value.vocabulary.code != '2':
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
        elif op == 'eq':
            if type(value) is not Sector:
                raise Exception('{} is not a sector'.format(value))
            if type(value.code) is CodelistItem:
                code = value.code.code
            else:
                code = value.code
            conditions = ['@code = "{code}"'.format(code=code)]
            if value.vocabulary is not None:
                conds = self.condition.get(value.vocabulary.code)
                conditions.append(self._vocab_condition(conds))
            return '{expr}[{conditions}]'.format(
                expr=self.get(),
                conditions=' and '.join(conditions),
            )
        return super().where(op, value)

    def exec(self, xml):
        return [Sector(x.get('code'),
                       vocabulary=x.get('vocabulary'),
                       percentage=x.get('percentage'))
                for x in xml.xpath(self.get())]
