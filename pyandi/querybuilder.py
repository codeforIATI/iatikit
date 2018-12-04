class QueryBuilder:
    def __init__(self, schema):
        self._schema = schema

    def where(self, **kwargs):
        exprs = []
        for shortcut, value in kwargs.items():
            if shortcut == 'xml':
                exprs.append(value)
                continue
            if '__' in shortcut:
                shortcut, operator = shortcut.split('__')
            else:
                operator = 'eq'
            # TODO
            expr = self._schema.get_query(shortcut, operator, value)
            exprs.append(expr)
        query_str = ''.join(['[{}]'.format(x) for x in exprs])
        return query_str

    def get(self, shortcut):
        # TODO
        return self._schema.get_query(shortcut)
