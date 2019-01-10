from os.path import abspath, dirname, join


def mod_join(*args):
    if args[0] == '__pyandicache__':
        path = join(dirname(abspath(__file__)), 'fixtures', *args[1:])
        return path
    if len(args) == 1:
        return args[0]
    return join(args[0], *args[1:])
