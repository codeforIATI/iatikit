from os.path import exists, join
import re

from lxml import etree as ET

from ..utils.exceptions import SchemaNotFoundError
from ..utils.validator import Validator, ValidationError
from ..utils.config import CONFIG


class XSDValidationError(ValidationError):
    def __init__(self, error, filetype, version):
        super(XSDValidationError, self).__init__(
            error.message, error.line, error.column, error.path)

        self.filetype = filetype
        self.version = version

    def _get_element(self):
        el_match = re.match(r"Element '([^']+)'", self.original_msg)
        return el_match.group(1) if el_match else None

    def _get_attribute(self):
        attr_match = re.search(r" attribute '([^']+)'", self.original_msg)
        return attr_match.group(1) if attr_match else None

    def _get_expecteds(self):
        expected_match = re.search(r'\( ([^)]+) \)', self.original_msg)
        if not expected_match:
            return []
        return [ex for ex in expected_match.group(1).split(', ')
                if not ex.startswith('##')]

    def _get_value(self):
        value_re = re.compile(r"Element '[^']+'(?:, attribute " +
                              r"'[^']+')?: '([^']*)'")
        value_match = value_re.match(self.original_msg)
        return value_match.group(1) if value_match else None

    @property
    def location(self):
        if self.column != 0:
            return 'Line {}, column {}.'.format(self.line, self.column)
        return 'Line {}.'.format(self.line)

    @property
    def url(self):
        if self.version in ['1.01', '1.02', '1.03']:
            # it's difficult to generate a URL for these
            return None
        path = re.sub(r'\[[^\]]+\]', '', self.path)
        tmpl = 'http://reference.iatistandard.org/{version}/' + \
               '{filetype}-standard{path}/'
        version_str = self.version.replace('.', '')
        return tmpl.format(version=version_str, path=path,
                           filetype=self.filetype)

    @property
    def message(self):
        tmpl = '{summary}\n\n{details}\n\n{location}'
        msg = tmpl.format(summary=self.summary, details=self.details,
                          location=self.location)
        url = self.url
        if url:
            msg += '\n\nSee: {url}'.format(url=url)
        return msg


class XSDDecimalTypeError(XSDValidationError):
    def __init__(self, error, filetype, version):
        super(XSDDecimalTypeError, self).__init__(error, filetype, version)

        value = self._get_value()

        # https://www.w3.org/TR/xmlschema-2/#decimal
        self.summary = 'An invalid decimal value is used.'
        if value is None:
            details = ''
        elif value == '':
            details = 'The value "{value}" is empty, which means ' + \
                      'it isn\'t a valid decimal value.'
        elif not any(map(lambda x: x.isdigit(), value)):
            details = 'The value "{value}" contains no digits at all, ' + \
                      'which means it isn\'t a valid decimal value.'
        elif ',' in value:
            details = 'The value "{value}" includes a comma, ' + \
                      'which isn\'t permitted.'
        elif '\x9c' in value:
            details = 'The value "{value}" includes the special ' + \
                      'character "\\x9c".'
        elif len(list(filter(lambda x: x.isdigit(), value))) > 18:
            details = 'The value "{value}" contains too many digits! ' + \
                      'It sounds ridiculous, but XML has a hard limit ' + \
                      'on the number of digits a decimal may contain.'
        else:
            details = 'The value "{value}" is not a valid decimal.'
        self.details = details.format(value=value)


class XSDDateTimeTypeError(XSDValidationError):
    def __init__(self, error, filetype, version):
        super(XSDDateTimeTypeError, self).__init__(error, filetype, version)

        value = self._get_value()

        # https://www.iso.org/iso-8601-date-and-time-format.html
        self.summary = 'An invalid "dateTime" is used.'
        details = 'Date and time values must use a very particular ' + \
                  'format, described by ISO 8601.'

        if value is not None:
            details += ' The following value does not adhere to that ' + \
                       'format: "{value}".'

        self.details = details.format(value=value)


class XSDDateTypeError(XSDValidationError):
    def __init__(self, error, filetype, version):
        super(XSDDateTypeError, self).__init__(error, filetype, version)

        value = self._get_value()

        # https://www.w3.org/TR/xmlschema-2/#date
        self.summary = 'An invalid date is used.'
        details = 'Dates must use a specific format (YYYY-MM-DD).'

        if value is not None:
            details += ' The following value does not fit that format: ' + \
                       '"{value}".'
        self.details = details.format(value=value)


class XSDBooleanTypeError(XSDValidationError):
    def __init__(self, error, filetype, version):
        super(XSDBooleanTypeError, self).__init__(error, filetype, version)

        value = self._get_value()
        attr = self._get_attribute()

        # https://www.w3.org/TR/xmlschema-2/#boolean
        self.summary = 'An invalid boolean (true or false) value ' + \
                       'is used.'
        details = 'The '
        if attr is not None:
            details += '"{attr_name}" attribute of the '
        details += '"{el_name}" element must be either "true", ' + \
                   '"false", "1" or "0". No other values are ' + \
                   'allowed.'

        if value is not None:
            if value.lower() in ['true', 'false']:
                details += ' The value used is "{value}", which is ' + \
                           'invalid because it is not all lowercase.'
            else:
                details += ' The value used instead is "{value}".'

        self.details = details.format(el_name=self._get_element(),
                                      attr_name=attr, value=value)


class XSDURITypeError(XSDValidationError):
    def __init__(self, error, filetype, version):
        super(XSDURITypeError, self).__init__(error, filetype, version)

        value = self._get_value()

        # https://www.w3.org/TR/xmlschema-2/#anyURI
        self.summary = 'An invalid link to a document or website ' + \
                       'is provided.'
        details = 'The following URL is used in the data, ' + \
                  'but is not valid: "{url}".'
        self.details = details.format(url=value)


class XSDNameTokenTypeError(XSDValidationError):
    def __init__(self, error, filetype, version):
        super(XSDNameTokenTypeError, self).__init__(error, filetype, version)

        value = self._get_value()
        attr = self._get_attribute()

        # https://www.w3.org/TR/xmlschema-2/#NMTOKEN
        self.summary = 'An invalid reference to another IATI ' + \
                       'element is used.'
        details = 'This is a bit unusual... The '
        if attr is not None:
            details += '"{attr_name}" attribute of the '

        details += '"{el_name}" element must reference another ' + \
                   ' IATI element.'

        if value is not None:
            details += ' However, the value provided ("{value}") ' + \
                       'is not a valid IATI element name.'
        self.details = details.format(el_name=self._get_element(),
                                      attr_name=attr, value=value)


class XSDTextNotAllowedError(XSDValidationError):
    def __init__(self, error, filetype, version):
        super(XSDTextNotAllowedError, self).__init__(error, filetype, version)

        self.summary = 'Text found where there shouldn\'t be any.'
        details = 'The "{el_name}" element is not allowed to contain ' + \
                  'any text. Either this text was added in error, or' + \
                  'should be included in an attribute or a ' + \
                  'child element.'
        self.details = details.format(el_name=self._get_element())


class XSDUnknownAttributeError(XSDValidationError):
    def __init__(self, error, filetype, version):
        super(XSDUnknownAttributeError, self).__init__(
            error, filetype, version)

        self.summary = 'An incorrect attribute is present.'
        details = 'The "{el_name}" element includes an attribute ' + \
                  '"{attr_name}". This attribute should not be ' + \
                  'present here.'
        self.details = details.format(el_name=self._get_element(),
                                      attr_name=self._get_attribute())


class XSDMissingAttributeError(XSDValidationError):
    def __init__(self, error, filetype, version):
        super(XSDMissingAttributeError, self).__init__(
            error, filetype, version)

        self.summary = 'A required attribute is missing.'
        details = 'The "{el_name}" element must include a ' + \
                  '"{attr_name}" attribute. This is missing.'
        self.details = details.format(el_name=self._get_element(),
                                      attr_name=self._get_attribute())


class XSDUnexpectedElementError(XSDValidationError):
    def __init__(self, error, filetype, version):
        super(XSDUnexpectedElementError, self).__init__(
            error, filetype, version)

        self.summary = 'An unexpected element was found.'
        expected = self._get_expecteds()
        if expected == []:
            expected_str = 'a different element'
        elif len(expected) == 1:
            expected_str = '"{}"'.format(expected[0])
        elif len(expected) == 2:
            expected_str = 'either "{}" or "{}"'.format(*expected)
        else:
            expected_str = 'one of "{}" or "{}"'.format(
                '", "'.join(expected[:-1]), expected[-1])

        if version.startswith('2'):
            details = 'In IATI v{version}, the order of elements ' + \
                      'is important. It looks like that might be ' + \
                      'the problem here. Specifically, ' + \
                      '"{el_name}" is present, but ' + \
                      '{expected} is expected.'
        else:
            details = 'The element "{el_name}" is present, but ' + \
                      '{expected} is expected.'
        self.details = details.format(version=version,
                                      expected=expected_str,
                                      el_name=self._get_element())


class XSDMissingElementError(XSDValidationError):
    def __init__(self, error, filetype, version):
        super(XSDMissingElementError, self).__init__(error, filetype, version)

        expected = self._get_expecteds()
        if expected == []:
            expected_str = 'a different element'
        elif len(expected) == 1:
            expected_str = '"{}"'.format(expected[0])
        else:
            expected_str = '"{}" and "{}"'.format(
                '", "'.join(expected[:-1]), expected[-1])

        if len(expected) > 1:
            self.summary = 'Some required elements are missing.'
            details = 'The "{el_name}" element expects some child ' + \
                      'elements, but these are missing. ' + \
                      'Specifically, {expected} are missing ' + \
                      'but should be present.'
        else:
            self.summary = 'A required element is missing.'
            details = 'The "{el_name}" element expects a child ' + \
                      'element, but this is missing. ' + \
                      'Specifically, {expected} is missing ' + \
                      'but should be present.'
        self.details = details.format(expected=expected_str,
                                      el_name=self._get_element())


class XSDBadRootNodeError(XSDValidationError):
    def __init__(self, error, filetype, version):
        super(XSDBadRootNodeError, self).__init__(error, filetype, version)

        el_name = self._get_element()

        self.summary = 'This doesn\'t look like an IATI XML dataset.'
        if 'microsoft.com' in el_name:
            details = 'It looks like this might be a Microsoft Office ' + \
                      'file, rather than an IATI XML dataset.'
            self.path = None
        else:
            details = 'The root node of the dataset should be either ' + \
                      '"iati-organisations" or "iati-activities". ' + \
                      'In this case, it is "{el_name}". That\'s a problem.'
        self.details = details.format(el_name=el_name)


class XSDValidator(Validator):
    def __init__(self, is_valid, errors, filetype, version):
        super(XSDValidator, self).__init__(is_valid, errors)

        self.filetype = filetype
        self.version = version

    @staticmethod
    def _get_error_class(ref, message):
        err_class = {
            1843: XSDTextNotAllowedError,
            1866: XSDUnknownAttributeError,
            1867: XSDUnknownAttributeError,
            1868: XSDMissingAttributeError,
            1845: XSDBadRootNodeError,
        }.get(ref)

        if not err_class:
            if ref == 1871:
                if 'This element is not expected.' in message:
                    err_class = XSDUnexpectedElementError
                elif 'Missing child element(s)' in message:
                    err_class = XSDMissingElementError
            elif ref == 1824:
                if 'atomic type \'xs:decimal\'' in message:
                    err_class = XSDDecimalTypeError
                elif 'atomic type \'xs:dateTime\'' in message:
                    err_class = XSDDateTimeTypeError
                elif 'atomic type \'xs:date\'' in message:
                    err_class = XSDDateTypeError
                elif 'atomic type \'xs:boolean\'' in message:
                    err_class = XSDBooleanTypeError
                elif 'atomic type \'xs:anyURI\'' in message:
                    err_class = XSDURITypeError
                elif 'atomic type \'xs:NMTOKEN\'' in message:
                    err_class = XSDNameTokenTypeError

        if not err_class:
            # Default: unknown schema error
            err_class = XSDValidationError

        return err_class

    @property
    def errors(self):
        error_list = []
        for error in self._errors:
            xsd_error_class = self._get_error_class(error.type,
                                                    error.message)
            xsd_error = xsd_error_class(error, self.filetype,
                                        self.version)
            error_list.append(xsd_error)
        return error_list

    @property
    def error_summary(self):
        error_dict = {}
        for error in self._errors:
            xsd_error_class = self._get_error_class(error.type,
                                                    error.message)
            error_type = xsd_error_class.__name__
            if error_type not in error_dict:
                xsd_error = xsd_error_class(error, self.filetype,
                                            self.version)
                error_dict[error_type] = [xsd_error, 1]
            else:
                error_dict[error_type][1] += 1
        return list(error_dict.values())


class XSDSchema(object):
    def __init__(self, filetype, version):
        self.filetype = filetype
        self.version = version

        schema = {
            'activity': 'iati-activities-schema.xsd',
            'organisation': 'iati-organisations-schema.xsd',
        }.get(filetype)

        if filetype is None:
            msg = 'Couldn\'t discern the filetype (activity or ' + \
                  'organisation) for this dataset, so couldn\'t ' + \
                  'construct a schema.'
            raise SchemaNotFoundError(msg)
        elif schema is None:
            msg = 'Invalid filetype "{filetype}" was provided, ' + \
                  'so couldn\'t construct a schema.'
            msg = msg.format(filetype=filetype)
            raise SchemaNotFoundError(msg)
        elif version is None:
            msg = 'No version was provided, ' + \
                  'so couldn\'t construct a schema.'
            raise SchemaNotFoundError(msg)

        self.schema_path = join(CONFIG['paths']['standard'], 'schemas',
                                version.replace('.', ''), schema)

        if not exists(self.schema_path):
            msg = 'No {filetype} schema found for IATI version "{version}".'
            msg = msg.format(filetype=filetype, version=version)
            raise SchemaNotFoundError(msg)

    def __repr__(self):
        return '<{} ({} {})>'.format(self.__class__.__name__,
                                     self.filetype, self.version)

    def validate(self, etree):
        schema = ET.XMLSchema(ET.parse(self.schema_path))
        is_valid = schema.validate(etree)
        return XSDValidator(is_valid, schema.error_log,
                            self.filetype, self.version)
