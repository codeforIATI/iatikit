import json
import logging
import os.path

from ..utils.exceptions import MappingsNotFoundError
from .codelist import CodelistSet


class CodelistMappings(object):
    def __init__(self, filetype, version, path=None):
        self.filetype = filetype
        self.version = version

        version_path = version.replace('.', '')
        if not path:
            path = os.path.join('__pyandicache__', 'standard',
                                'codelist_mappings')
        self.mappings_path = os.path.join(path, version_path,
                                          '{}-mappings.json'.format(filetype))

        if not os.path.exists(self.mappings_path):
            msg = 'No codelist mappings found for IATI version "{version}".'
            msg = msg.format(version=version)
            raise MappingsNotFoundError(msg)

    def __repr__(self):
        return '<{} ({} {})>'.format(self.__class__.__name__,
                                     self.filetype, self.version)

    def validate(self, dataset):
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

        with open(self.mappings_path) as handler:
            mappings = json.load(handler)

        success = True
        for mapping in mappings:
            xpath_query, codelist = parse_mapping(mapping)
            values = dataset.etree.xpath(xpath_query)
            for value in set(values):
                if not codelist.get(value):
                    msg = '"%s" not in %s codelist.'
                    logging.warning(msg, value, codelist.name)
                    success = False
        return success
