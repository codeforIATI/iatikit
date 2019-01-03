from os.path import abspath, dirname, join


def mod_join(*args):
    if '/'.join(args) == '__pyandicache__/standard/codelists':
        path = join(dirname(abspath(__file__)), 'fixtures', 'codelists')
        return path
    else:
        return join(*args)
