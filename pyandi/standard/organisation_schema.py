# from ..utils.exceptions import SchemaError
# from ..utils.types import StringType


# class OrganisationSchema101(object):
#     version = '1.01'

#     @classmethod
#     def org_identifier(cls):
#         return StringType('iati-identifier/text()')


# class OrganisationSchema102(OrganisationSchema101):
#     version = '1.02'


# class OrganisationSchema103(OrganisationSchema102):
#     version = '1.03'


# class OrganisationSchema104(OrganisationSchema103):
#     version = '1.04'


# class OrganisationSchema105(OrganisationSchema104):
#     version = '1.05'


# class OrganisationSchema201(OrganisationSchema105):
#     version = '2.01'

#     @classmethod
#     def org_identifier(cls):
#         return StringType('organisation-identifier/text()')


# class OrganisationSchema202(OrganisationSchema201):
#     version = '2.02'


# class OrganisationSchema203(OrganisationSchema202):
#     version = '2.03'


# def get_organisation_schema(version):
#     if version == '2.03':
#         return OrganisationSchema203
#     elif version == '2.02':
#         return OrganisationSchema202
#     elif version == '2.01':
#         return OrganisationSchema201
#     elif version == '1.05':
#         return OrganisationSchema105
#     elif version == '1.04':
#         return OrganisationSchema104
#     elif version == '1.03':
#         return OrganisationSchema103
#     elif version == '1.02':
#         return OrganisationSchema102
#     elif version == '1.01':
#         return OrganisationSchema101

#     msg = 'Unknown organisation schema: version: {}'.format(version)
#     raise SchemaError(msg)
