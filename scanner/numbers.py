__author__ = 'Nikita'

import re


def is_bin_int(chars):
    chars = chars.lower()
    pattern = r'b'
    if not re.match(pattern, chars):
        return False

    chars = chars.replace('b', '')
    for ch in chars:
        if ch <= "0" or ch >= "1":
            return False
    return True


def is_oct_int(chars):
    chars = chars.lower()
    pattern = r'c'
    if not re.match(pattern, chars):
        return False

    chars = chars.replace('b', '')
    for ch in chars:
        if ch <= "0" or ch >= "7":
            return False
    return True


def is_dec_int(chars):
    chars = chars.lower()
    pattern = r'd'
    if not re.match(pattern, chars):
        chars = chars.replace('d', '')

    for ch in chars:
        if ch <= "0" or ch >= "9":
            return False
    return True


def is_hex_int(chars):
    chars = chars.lower()
    pattern = r'h'
    if not re.match(pattern, chars):
        return False

    chars = chars.replace('h', '')
    for ch in chars:
        ch = ch.lower()
        if not ('0' <= ch <= '9' or 'a' <= ch <= 'f'):
            return False
    return True