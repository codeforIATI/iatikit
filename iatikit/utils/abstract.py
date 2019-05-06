from copy import deepcopy
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
    _multi_filters = []
    _instance_class = None

    def __init__(self, **kwargs):
        self.wheres = {}
        self.where(**kwargs)

    def where(self, **kwargs):
        """Return a new set, with the filters provided in ``**kwargs``.
        """
        out = deepcopy(self)
        for k, v in kwargs.items():
            if k.split('__')[0] not in (self._filters + self._multi_filters):
                raise FilterError('Unknown filter: {}'.format(k))
            if k.split('__')[0] in self._filters:
                if k in out.wheres:
                    raise FilterError('Too many {} filters provided'.format(k))
                out.wheres[k] = v
            else:
                if k not in out.wheres:
                    out.wheres[k] = []
                out.wheres[k].append(v)
        return out

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
        """
        return list(x for x in self)

    def get(self, item, default=None):
        """Return an item from the set, according to the primary key.

        If no matching item is found, ``default`` is returned.
        """
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
