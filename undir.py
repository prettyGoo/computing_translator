import sys
import re

from lexems_automats.key_words import *
from lexems_automats.numbers import is_digit, is_hex_digit
from lexems_automats.sintaksis import is_space, is_new_line, is_eof

from lexems_printer import print_lexeme

try:
    file = open('code.txt', 'r')
except FileNotFoundError:
    print('Aborted: the file you are looking for does not exist\n')
    sys.exit(0)

lexema = 'NoLex'
row = 1
base_position = 0
offset = 1


def is_letter(char):
    return 'a' <= char <= 'z'


def is_id_or_kw():
    global lexema
    global base_position
    global offset

    local_lexeme = ''
    local_offset = 0

    char = file.read(1)

    if is_letter(char):
        while True:
            file.seek(base_position)
            chars = file.read(local_offset+1).lower()
            local_offset += 1

            if is_kw_write(chars):
                local_lexeme = 'Write'
                break

            if is_kw_read(chars):
                local_lexeme = 'Read'
                break
        char = file.read(1)
        if not is_digit(char):
            if not is_letter(char):
                offset = local_offset
                lexema = local_lexeme
                return True
        local_offset += 1
        while True:
            char = file.read(1).lower()
            if not (is_letter(char) or is_digit(char)):
                offset = local_offset
                lexema = 'Id'
                break
            local_offset += 1
        return True
    else:
        file.seek(base_position)
        return False


def is_dec_int():
    global base_position
    global offset

    new_offset = 1
    char = file.read(1)
    if is_digit(char):
        while True:
            char = file.read(1)
            if is_digit(char):
                new_offset += 1
            else:
                break
        if not is_letter(char):
            offset = new_offset
            return True
        else:
            return False
    else:
        return False


def seek_new_position():
    global base_position
    global offset

    base_position = file.tell()
    offset = 1


# def get_next_char(with_offset=False):
#     global offset
#
#     next_char = file.read(1).lower()
#     if with_offset:
#         offset += 1
#
#     return next_char
#
#
# def get_next_chars(with_offset=False):
#     global offset
#
#     next_chars = file.read(offset).lower()
#     if with_offset:
#         offset += 1
#     return next_chars


def get_next_lexema():

    global lexema

    global base_position
    global offset
    global row

    while True:  # while no stop char have been met
        char = file.read(1).lower()

        if is_eof(char):
            lexema = 'EOF'
            return lexema

        if is_space(char):
            lexema = 'Space'
            base_position = file.tell()
            offset = 1
            return lexema

        if is_new_line(char):
            lexema = 'NewLine'
            base_position = file.tell()
            offset = 1
            row += 1
            seek_new_position()
            return lexema
        """ if no split char was detected it means that the char is valuable and file position must be unset """
        file.seek(base_position)

        """ read inside automata """
        if is_dec_int():
            lexema = 'DecInt'
            base_position += offset
            file.seek(base_position)
            return lexema
        file.seek(base_position)

        if is_id_or_kw():
            base_position += offset
            file.seek(base_position)
            return lexema
        file.seek(base_position)
        # chars = file.read(offset).lower()
        # offset += 1
        #
        # # """ read inside automata """
        # if is_kw_write(chars):
        #     lexema = 'Write'
        #     seek_new_position()
        #     return lexema
        #
        # if is_kw_read(chars):
        #     lexema = 'Read'
        #     seek_new_position()
        #     return lexema


while True:
    if not lexema == 'EOF':
        lexema = get_next_lexema()
        print_lexeme(row, lexema)
    else:
        break

print('====== Scanning has been finished ======')