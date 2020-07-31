from ..utils.abstract import GenericSet


class Transaction(object):
    pass


class TransactionSet(GenericSet):
    """Class representing a grouping of ``Transaction`` objects.

    Objects in this grouping can be filtered and iterated over.
    Queries are only constructed and run when needed, so they
    can be efficient.
    """

    _key = 'ref'
    _instance_class = Transaction
    _filetype = 'activity'
    _element = '/iati-activities/iati-activity/transaction'
