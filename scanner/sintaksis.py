__author__ = 'Nikita'


def is_space(ch):
    return ch == ' '


def is_tab(ch):
    return ch == '\x09'


def is_skip(ch):
    return ch == '\x10'


def is_comma(ch):
    return ch == ','


def is_colon(ch):
    return ch == ':'


def is_semicolon(ch):
    return ch == ':'


def is_eot(ch):
    return ch == '\x03'
