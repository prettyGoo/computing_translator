__author__ = 'Nikita'


def is_digit(char):
    return '0' <= char <= '9'


def is_bin_digit(char):
    return '0' <= char <= '1'


def is_oct_digit(char):
    return '0' <= char <= '7'


def is_hex_digit(char):
    return '0' <= char <= '9' or 'a' <= char <= 'f'


def is_letter(char):
    return 'a' <= char <= 'z' or char == '_'
