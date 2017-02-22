__author__ = 'Nikita'




# TODO Numbers and IDS
def is_digit(ch):
    return '0' <= ch <= '9'


def is_id(ch):
    return 'a' <= ch.lower() <= 'z'  # TODO replace for abc1

# TODO Sintaksis
def is_space(ch):
    return ch == ' '


def is_comma(ch):
    return ch == ','


def is_colon(ch):
    return ch == ':'


def is_semicolon(ch):
    return ch == ':'


# TODO Keywords
def is_kw_write(ch):
    return ch.lower() == 'write'


def is_kw_read(ch):
    return ch.lower() == 'read'


def is_kw_end(ch):
    return ch.lower() == 'end'


def is_kw_goto(ch):
    return ch.lower() == 'goto'
