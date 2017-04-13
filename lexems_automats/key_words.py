__author__ = 'Nikita'


def is_kw_write(chars):
    return chars.lower() == 'write'


def is_kw_read(ch):
    return ch.lower() == 'read'


def is_kw_end(ch):
    return ch.lower() == 'end'


def is_kw_goto(ch):
    return ch.lower() == 'goto'


def is_kw_while(ch):
    return ch.lower() == 'while'


def is_kw_loop(ch):
    return ch.lower() == 'loop'


def is_kw_do(ch):
    return ch.lower() == 'do'
