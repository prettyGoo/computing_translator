import sys
import re

from lexems_automats.key_words import *
# from lexems_automats.numbers import
from lexems_automats.sintaksis import is_space, is_new_line, is_eof

try:
    file = open('code.txt', 'r')
except FileNotFoundError:
    print('Aborted: the file you are looking for does not exist\n')
    sys.exit(0)

lexema = 'NoLex'
row = 1
base_position = 0
offset = 1


def is_digit(char):
    return '0' <= char <= '9'


def is_letter(char):
    return 'a' <= char <= 'z'


def is_dec_int():
    global base_position
    global offset

    char = file.read(1)
    offset += 1
    while is_digit(char):
        char = file.read(1)
        offset += 1
    if not is_letter(char):
        return True
    else:
        return False


def print_lexema(lexema):
    if lexema == 'Write':
        print('%s\tWRITE' % row)
    elif lexema == 'Read':
        print('%s\tREAD' % row)
    elif lexema == 'NewLine':
        print('%s\tSPACE' % row)
    elif lexema == 'EOF':
        print('%s\tEOF' % row)


def unset():
    global base_position
    global offset

    file.seek(base_position)
    offset = 1


def seek_new_position():
    global base_position
    global offset

    base_position = file.tell()
    offset = 1


def get_next_char():
    global offset

    next_char = file.read(1)
    return next_char


def get_next_chars():
    global offset

    next_chars = file.read(offset)
    return next_chars


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
            seek_new_position()
            break

        if is_new_line(char):
            row += 1
            seek_new_position()
            break
        unset()


        if is_dec_int():
            lexema = 'DECINT'
            seek_new_position()
            return lexema
        unset()

        chars = file.read(offset).lower()
        offset += 1

        if is_kw_write(chars):
            lexema = 'Write'
            seek_new_position()
            return lexema

        if is_kw_read(chars):
            lexema = 'Read'
            seek_new_position()
            return lexema

while True:
    if not lexema == 'EOF':
        lexema = get_next_lexema()
        print_lexema(lexema)
    else:
        break

print('====== Scanning has been finished ======')