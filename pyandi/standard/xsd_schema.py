import json
import logging
import os.path

from lxml import etree

from ..utils.exceptions import SchemaNotFoundError
from .codelist import CodelistSet


class XSDSchema(object):
    def __init__(self, filetype, version, path=None):
        self.filetype = filetype
        self.version = version

        schema = {
            'activity': 'iati-activities-schema.xsd',
            'organisation': 'iati-organisations-schema.xsd',
        }.get(filetype)

        version_path = version.replace('.', '')
        if not path:
            path = os.path.join('__pyandicache__', 'standard', 'schemas')
        schema_path = os.path.join(path, version_path, schema)

        if not os.path.exists(schema_path):
            msg = 'No {filetype} schema found for IATI version "{version}".'
            msg = msg.format(filetype=filetype, version=version)
            raise SchemaNotFoundError(msg)

        self.schema = etree.XMLSchema(etree.parse(schema_path))

        self.mappings_path = os.path.join(path, version_path, 'mapping.json')

    def __repr__(self):
        return '<{} ({} {})>'.format(self.__class__.__name__,
                                     self.filetype, self.version)

    def validate(self, dataset):
        is_valid = self.schema.validate(dataset.etree)
        if not is_valid:
            logging.warning(self.schema.error_log)
        return is_valid

    def validate_codelists(self, dataset):
        codelists = CodelistSet()

        def parse_mapping(mapping):
            condition = mapping.get('condition')
            if condition:
                path_body, path_head = mapping['path'].rsplit('/', 1)
                path = '{path_body}[{condition}]/{path_head}'.format(
                    path_body=path_body,
                    condition=condition,
                    path_head=path_head,
                )
            else:
                path = mapping['path']
            return path, codelists.get(mapping['codelist'])

        if not os.path.exists(self.mappings_path):
            msg = 'Can\'t perform codelist validation for IATI version %s.'
            logging.warning(msg, self.version)
            return True

        with open(self.mappings_path) as handler:
            mappings = json.load(handler)

        success = True
        for mapping in mappings:
            xpath_query, codelist = parse_mapping(mapping)
            values = dataset.etree.xpath(xpath_query)
            for value in values:
                if not codelist.get(value):
                    msg = '"%s" not in %s codelist.'
                    logging.warning(msg, value, codelist.name)
                    success = False
        return success
