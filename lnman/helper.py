def ref_keys(keys):
    return 'config' + ''.join(['[{}]'.format(repr(k)) for k in keys])

def term_cyan(s):
    return "\033[0;36m" + s + "\033[0m"