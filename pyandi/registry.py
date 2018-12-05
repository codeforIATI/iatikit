from os.path import join

from .publisher import PublisherSet


class Registry:
    def __init__(self):
        self.path = join('__pyandicache__', 'data')

    @property
    def publishers(self):
        return PublisherSet(self.path)


def publishers():
    return Registry().publishers
