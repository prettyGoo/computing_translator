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


def Is_let(chars):
    last_char = chars[-1]
    if chars.replace(last_char, '') == ':=':
        if not is_single_math_sign(last_char):
            return True, ':='
        else:
            return False, {'lexeme': 'Error', 'error': 'wrong math combination', 'value': chars}
    return False, None


def Is_ne(chars):
    last_char = chars[-1]
    if chars.replace(last_char, '') == '<>':
        if not is_single_math_sign(last_char):
            return True, '<>'
        else:
            return False, {'lexeme': 'Error', 'error': 'wrong math combination', 'value': chars}
    return False, None


def Is_le(chars):
    last_char = chars[-1]
    if chars.replace(last_char, '') == '<=':
        if not is_single_math_sign(last_char):
            return True, '<='
        else:
            return False, {'lexeme': 'Error', 'error': 'wrong math combination', 'value': chars}
    else:
        return False, None


def Is_ge(chars):
    last_char = chars[-1]
    if chars.replace(last_char, '') == '>=':
        if not is_single_math_sign(last_char):
            return True, '>='
        else:
            return False, {'lexeme': 'Error', 'error': 'wrong math combination', 'value': chars}
    else:
        return False, None


def is_eq(chars):
    return chars[0] == '=' and not is_single_math_sign(chars[1])


def is_lt(chars):
    return chars[0] == '<' and not is_single_math_sign(chars[1])


def is_gt(chars):
    return chars[0] == '>' and not is_single_math_sign(chars[1])


def is_single_math_sign(char):
    return char in '<>=+-/*'
