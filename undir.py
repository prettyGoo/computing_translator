import sys
import re

from lexems_automats.key_words import *
from lexems_automats.numbers import is_dec_int
from lexems_automats.sintaksis import is_space, is_new_line, is_eof

try:
    file = open('code.txt', 'r')
except FileNotFoundError:
    print('Aborted: the file you are looking for does not exist\n')
    sys.exit(0)

lexema = 'NoLex'
row = 1
base_position = 0
offset = 0


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
    # global base_position
    # global offset

    file.seek(base_position)
    offset = base_position + 1


def seek_new_position():
    global base_position
    global offset
    base_position += (offset + 1)
    file.seek(base_position)


def is_new_line(char):
    return char == '\n'



def is_eof(char):
    return not char  # empty string - EOF - is always False


def get_next_char():
    global offset
    global row

    offset += 1
    next_char = file.read(1)
    return next_char


def get_next_lexema():

    global base_position
    global offset
    global row


    lexema = 'EmptyLex'
    while True:  # while no stop char have been met
        char = get_next_char().lower()

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
        chars = file.read(offset-base_position).lower()

        if is_dec_int(chars):
            lexema = 'Integer'
            seek_new_position()
            return lexema

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