from .registry import Registry


def publishers():
    return Registry().publishers()
