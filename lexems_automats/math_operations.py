__author__ = 'Nikita'

from lexems_automats.sintaksis import *


def is_add(char):
    return char == '+'


def is_min(char):
    return char == '-'


def is_mul(char):
    return char == '*'


def is_div(char):
    return char == '/'


def is_let(chars):
    last_char = chars[-1]
    return chars.replace(last_char, '') == ':=' and is_split(last_char)


def is_not_eq(chars):
    last_char = chars[-1]
    return chars.replace(last_char, '') == '<>' and is_split(last_char)


def is_le(chars):
    last_char = chars[-1]
    return chars.replace(last_char, '') == '<=' and is_split(last_char)


def is_ge(chars):
    last_char = chars[-1]
    return chars.replace(last_char, '') == '>=' and is_split(last_char)


def is_eq(char):
    return char == '='


def is_ne(char):
    return char == '<>'


def is_lt(char):
    return char == '<'


def is_gt(char):
    return char == '>'
