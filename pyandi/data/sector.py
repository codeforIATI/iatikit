from ..standard.codelist import CodelistSet, CodelistItem


class Sector(object):
    def __init__(self, code, vocabulary=None, percentage=None):
        codelists = CodelistSet()

        if percentage is not None:
            self.percentage = float(percentage)
        else:
            self.percentage = None

        if vocabulary:
            vocab_item = codelists.get('Vocabulary').get(vocabulary)
            if vocab_item is not None:
                new_code = {
                    'ADT': '6', 'COFOG': '3',
                    'DAC': '1', 'DAC-3': '2',
                    'ISO': None, 'NACE': '4',
                    'NTEE': '5', 'RO': '99',
                    'RO2': '98', 'WB': None,
                }.get(vocab_item.code)
                if new_code:
                    vocab_item = codelists.get(
                        'SectorVocabulary').get(new_code)
            else:
                vocab_item = codelists.get('SectorVocabulary').get(vocabulary)
                if vocab_item is None:
                    raise Exception('Unknown vocabulary')
            if vocab_item.code in ['DAC', '1']:
                self.code = codelists.get('Sector').get(code)
            elif vocab_item.code in ['DAC-3', '2']:
                self.code = codelists.get('SectorCategory').get(code)
            else:
                self.code = str(code)
            if self.code is None:
                raise Exception('Code and vocabulary don\'t match')
            self.vocabulary = vocab_item
        else:
            if type(code) is CodelistItem:
                if code.codelist.slug == 'Sector':
                    self.vocabulary = codelists.get(
                        'SectorVocabulary').get('1')
                elif code.codelist.slug == 'SectorCategory':
                    self.vocabulary = codelists.get(
                        'SectorVocabulary').get('2')
                else:
                    raise Exception('Invalid sector code: {}'.format(code))
                self.code = code
            else:
                self.code = str(code)
                self.vocabulary = None

    def __repr__(self):
        if type(self.code) is CodelistItem:
            txt = '{} ({}), Vocabulary: {}'.format(
                self.code.name, self.code.code, self.vocabulary.name)
        else:
            if self.vocabulary:
                txt = '{}, Vocabulary: {}'.format(
                    self.code, self.vocabulary.name)
            else:
                txt = '{}, Vocabulary: Unspecified'.format(self.code)
        return '<{} ({})>'.format(self.__class__.__name__, txt)
