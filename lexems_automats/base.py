__author__ = 'Nikita'


def is_digit(char):
    a = '0' <= char <= '9'
    return '0' <= char <= '9'


def is_hex_digit(char):
    return 'a' <= char <= 'f'


def is_letter(char):
    return 'a' <= char <= 'z' or char == '_'
