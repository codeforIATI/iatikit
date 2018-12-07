from os.path import join

import xmlschema


class Schema:
    def __init__(self, version, path=None):
        if path:
            self.path = path
        else:
            self.path = join('__pyandicache__', 'standard', 'schemas')
        self._schema = None

    @property
    def schema(self):
        if not self._schema:
            self._schema = xmlschema.XMLSchema(self.schema_path)
        return self._schema

    def find(self, search):
        return self.schema.find(search)


class OrganisationSchema(Schema):
    def __init__(self, version):
        super().__init__(version)
        self.schema_path = join(self.path, version,
                                'iati-organisations-schema.xsd')


class ActivitySchema(Schema):
    def __init__(self, version):
        super().__init__(version)
        self.schema_path = join(self.path, version,
                                'iati-activities-schema.xsd')
