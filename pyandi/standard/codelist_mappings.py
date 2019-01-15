import json
from os.path import exists, join

from ..utils.exceptions import MappingsNotFoundError
from ..utils.validator import Validator
from ..utils.config import CONFIG
from .codelist import CodelistSet


class CodelistMappings(object):
    def __init__(self, filetype, version):
        self.filetype = filetype
        self.version = version

        version_path = version.replace('.', '')
        self.mappings_path = join(CONFIG['paths']['standard'],
                                  'codelist_mappings', version_path,
                                  '{}-mappings.json'.format(filetype))

        if not exists(self.mappings_path):
            tmpl = 'No codelist mappings found for IATI version ' + \
                   '"{version} ({filetype})".'
            msg = tmpl.format(version=version, filetype=filetype)
            raise MappingsNotFoundError(msg)

    def __repr__(self):
        return '<{} ({} {})>'.format(self.__class__.__name__,
                                     self.filetype, self.version)

    def validate(self, dataset):
        codelists = CodelistSet(version=dataset.version)

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
        error_log = []
        for mapping in mappings:
            xpath_query, codelist = parse_mapping(mapping)
            values = dataset.etree.xpath(xpath_query)
            for value in set(values):
                if not codelist.get(value):
                    error = '"{}" not in {} codelist.'.format(
                        value, codelist.name)
                    error_log.append(error)
                    success = False
        return Validator(success, error_log)
