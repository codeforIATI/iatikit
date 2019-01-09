import logging
import os.path

from lxml import etree

from ..utils.exceptions import SchemaNotFoundError


class XSDSchema(object):
    def __init__(self, filetype, version, path=None):
        self.filetype = filetype
        self.version = version

        schema = {
            'activity': 'iati-activities-schema.xsd',
            'organisation': 'iati-organisations-schema.xsd',
        }.get(filetype)

        if not path:
            path = os.path.join('__pyandicache__', 'standard', 'schemas')
        self.path = os.path.join(path, version.replace('.', ''), schema)

        if not os.path.exists(self.path):
            msg = 'No {filetype} schema found for IATI version "{version}".'
            msg = msg.format(filetype=filetype, version=version)
            raise SchemaNotFoundError(msg)

        self.schema = etree.XMLSchema(etree.parse(self.path))

    def __repr__(self):
        return '<{} ({} {})>'.format(self.__class__.__name__,
                                     self.filetype, self.version)

    def validate(self, dataset):
        is_valid = self.schema.validate(dataset.etree)
        if not is_valid:
            logging.warning(self.schema.error_log)
        return is_valid
