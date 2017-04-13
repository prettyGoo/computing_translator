__author__ = 'Nikita'


def is_kw_write(chars):
    return chars == 'write', 'Write'


def is_kw_read(chars):
    return chars == 'read', 'Read'


def is_kw_end(chars):
    return chars == 'end', 'End'


def is_kw_goto(chars):
    return chars == 'goto', 'Goto'


def is_kw_while(chars):
    return chars == 'while', 'While'


def is_kw_loop(chars):
    return chars == 'loop', 'Loop'


def is_kw_do(chars):
    return chars == 'do', 'Do'
