def ref_keys(keys):
    return 'config' + ''.join(['[{}]'.format(repr(k)) for k in keys])

def term_color(s, col):
    ctable = {
        'cyan': '\033[0;36m',
        'yellow': '\033[1;33m',
        'green': '\033[1;32m',
        'red': '\033[1;31m',
    }

    return ''.join([ctable[col], s, '\033[0m'])

