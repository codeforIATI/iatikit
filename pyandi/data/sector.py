from ..standard.codelist import CodelistSet, CodelistItem
from ..utils.exceptions import UnknownSectorVocabError, \
                               UnknownSectorCodeError, InvalidSectorCodeError


class Sector(object):
    def __init__(self, code, vocabulary=None, percentage=None):
        codelists = CodelistSet()
        vocab_lookup = {
            '1': 'Sector',
            '2': 'SectorCategory',
        }

        def get_vocabulary(vocabulary_code):
            old_vocab_item = codelists.get(
                'Vocabulary').get(vocabulary_code)

            if old_vocab_item is not None:
                new_vocab_code = {
                    'ADT': '6', 'COFOG': '3',
                    'DAC': '1', 'DAC-3': '2',
                    'ISO': None, 'NACE': '4',
                    'NTEE': '5', 'RO': '99',
                    'RO2': '98', 'WB': None,
                }.get(old_vocab_item.code)
                if new_vocab_code:
                    vocab_item = codelists.get(
                        'SectorVocabulary').get(new_vocab_code)
            else:
                vocab_item = codelists.get(
                    'SectorVocabulary').get(vocabulary_code)
                if vocab_item is None:
                    raise UnknownSectorVocabError()
            return vocab_item

        if percentage is not None:
            self.percentage = float(percentage)
        else:
            self.percentage = None

        if isinstance(code, CodelistItem):
            if code.codelist.slug == 'Sector':
                self.vocabulary = codelists.get(
                    'SectorVocabulary').get('1')
            elif code.codelist.slug == 'SectorCategory':
                self.vocabulary = codelists.get(
                    'SectorVocabulary').get('2')
            else:
                raise InvalidSectorCodeError(
                    'Not a sector code: {}'.format(code))
            self.code = code
        elif vocabulary:
            self.vocabulary = get_vocabulary(vocabulary)

            vocab_codelist_name = vocab_lookup.get(self.vocabulary.code)
            if vocab_codelist_name:
                self.code = codelists.get(vocab_codelist_name).get(code)
                if self.code is None:
                    raise UnknownSectorCodeError()
            else:
                self.code = str(code)
        else:
            self.code = str(code)
            self.vocabulary = None

    def __repr__(self):
        if isinstance(self.code, CodelistItem):
            txt = '{} ({}), Vocabulary: {}'.format(
                self.code.name, self.code.code, self.vocabulary.name)
        else:
            if self.vocabulary:
                txt = '{}, Vocabulary: {}'.format(
                    self.code, self.vocabulary.name)
            else:
                txt = '{}, Vocabulary: Unspecified'.format(self.code)
        return '<{} ({})>'.format(self.__class__.__name__, txt)

    def __eq__(self, value):
        if not isinstance(value, Sector):
            return False
        if self.vocabulary and self.vocabulary != value.vocabulary:
            return False
        if self.code and self.code != value.code:
            return False
        if self.percentage != value.percentage:
            return False
        return True

    def __ne__(self, value):
        return not self.__eq__(value)
