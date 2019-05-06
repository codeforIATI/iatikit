class XPathQueryBuilder(object):
    def __init__(self, schema, prefix='', count=False):
        self._schema = schema
        self._count = count
        self._prefix = prefix

    def where(self, **kwargs):
        query_str = self._prefix

        exprs = []
        for shortcut, values in kwargs.items():
            if '__' in shortcut:
                shortcut, operator = shortcut.split('__')
            else:
                operator = 'eq'
            for value in values:
                expr = self.filter(shortcut, operator, value)
                exprs.append(expr)
        query_str += ''.join(['[{}]'.format(x) for x in exprs])
        if self._count:
            query_str = 'count({})'.format(query_str)
        return query_str

    def filter(self, shortcut, operator, value):
        return getattr(self._schema, shortcut)().where(operator, value)
