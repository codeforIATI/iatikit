from itertools import islice
from .exceptions import OperationError, FilterError, NotFoundError


class GenericSet(object):
    def __init__(self):
        self._key = None
        self._filters = []
        self._wheres = {}
        self._instance_class = None

    def where(self, **kwargs):
        for k in kwargs.keys():
            if k.split('__')[0] not in self._filters:
                raise FilterError('Unknown filter: {}'.format(k))
        self._wheres = dict(self._wheres, **kwargs)
        return self

    def filter(self, **kwargs):
        return self.where(**kwargs)

    def __getitem__(self, index):
        try:
            return next(islice(self, index, index + 1))
        except TypeError:
            return list(islice(self, index.start, index.stop, index.step))

    def __len__(self):
        total = 0
        for x in self:
            total += 1
        return total

    def count(self):
        return len(self)

    def first(self):
        for first in self:
            return first
        raise NotFoundError

    def all(self):
        return list(iter(self))

    def get(self, item, default=None):
        if type(item) is self._instance_class:
            item = getattr(item, self._key)
        try:
            return self.find(**{self._key: item})
        except NotFoundError:
            return default

    def find(self, **kwargs):
        return self.where(**kwargs).first()


class GenericType(object):
    def __init__(self, expr):
        self._expr = expr

    def get(self):
        return self._expr

    def run(self, etree):
        return etree.xpath(self.get())

    def where(self, op, value):
        if op == 'exists':
            subop = '!= 0' if value else '= 0'
            return 'count({expr}) {subop}'.format(
                expr=self.get(),
                subop=subop,
            )
        elif op == 'eq':
            return '{expr} = "{value}"'.format(
                expr=self.get(),
                value=value,
            )
        raise OperationError('Unknown operation: {}'.format(op))
