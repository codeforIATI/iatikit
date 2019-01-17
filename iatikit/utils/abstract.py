from copy import copy
from itertools import islice
from .exceptions import FilterError


class GenericSet(object):
    """Class representing a generic grouping of iatikit objects.

    Objects in this grouping can be filtered and iterated over.
    Queries are only constructed and run when needed, so they
    can be efficient.
    """

    _key = None
    _filters = []
    _instance_class = None

    def __init__(self):
        self.wheres = {}

    def where(self, **kwargs):
        """Return a new set, with the filters provided in ``**kwargs``.
        """
        for k in kwargs:
            if k.split('__')[0] not in self._filters:
                raise FilterError('Unknown filter: {}'.format(k))
        clone = copy(self)
        clone.wheres = dict(clone.wheres, **kwargs)
        return clone

    def filter(self, **kwargs):
        """Return a new set, with the filters provided in ``**kwargs``.

        Alias of ``where(**kwargs)``.
        """
        return self.where(**kwargs)

    def __getitem__(self, index):
        try:
            return next(islice(self, index, index + 1))
        except TypeError:
            return list(islice(self, index.start, index.stop, index.step))
        except StopIteration:
            pass
        raise IndexError('index out of range')

    def __len__(self):
        return sum(1 for x in self)

    def count(self):
        """The number of items in this set.

        Equivalent to ``len(self)``.
        """
        return len(self)

    def first(self):
        """Return the first item in this set.

        Raises an ``IndexError`` if the set contains zero items.

        Equivalent to ``self[0]``.
        """
        return self[0]

    def all(self):
        """Return a list of all items in this set.

        Equivalent to ``list(self)``.
        """
        return list(self)

    def get(self, item, default=None, fast=False):
        """Return an item from the set, according to the primary key.

        If no matching item is found, ``default`` is returned.
        """
        if fast:
            msg = 'The `fast` keyword argument can\'t be used here.'
            raise NotImplementedError(msg)
        if isinstance(item, self._instance_class):
            item = getattr(item, self._key)
        try:
            return self.find(**{self._key: item})
        except IndexError:
            return default

    def find(self, **kwargs):
        """Return the first matching item from the set, according to the
        filters provided in ``kwargs``.

        If no matching item is found, an ``IndexError`` is raised.

        ``find(**kwargs)`` is equivalent to ``where(**kwargs).first()``.
        """
        return self.where(**kwargs).first()


class GenericType(object):
    def __init__(self, expr):
        self._expr = expr

    def get(self):
        return self._expr

    def run(self, etree):
        return etree.xpath(self.get())

    def where(self, operation, value):
        if operation == 'exists':
            sub_operation = '!= 0' if value else '= 0'
            return 'count({expr}) {subop}'.format(
                expr=self.get(),
                subop=sub_operation,
            )
        elif operation == 'eq':
            return '{expr} = "{value}"'.format(
                expr=self.get(),
                value=value,
            )
        raise FilterError('Unknown filter modifier: {}'.format(operation))
