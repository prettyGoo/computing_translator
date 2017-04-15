__author__ = 'Nikita'


def is_eof(ch):
    return not ch


def is_space(ch):
    return ch == ' '


def is_tab(ch):
    return ch == '\t'


def is_new_line(ch):
    return ch == '\n'


def is_split(ch):
    return is_space(ch) or is_tab(ch) or is_new_line(ch) or is_eof(ch)


def is_comma(ch):
    return ch == ','


def is_colon(ch):
    return ch == ':'


def is_semicolon(ch):
    return ch == ';'


def is_starting_comment(char):
    return char == '{'


def is_finishing_comment(char):
    return char == '}'
