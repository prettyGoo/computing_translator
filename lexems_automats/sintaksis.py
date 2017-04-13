__author__ = 'Nikita'


def is_space(ch):
    return ch == ' '


def is_tab(ch):
    return ch == '\t'


def is_new_line(ch):
    return ch == '\n'


def is_comma(ch):
    return ch == ','


def is_colon(ch):
    return ch == ':'


def is_semicolon(ch):
    return ch == ';'


def is_eof(ch):
    return not ch
