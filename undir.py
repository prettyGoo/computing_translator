import sys

from lexems_automats.indetificators import Is_id_or_kw
from lexems_automats.numbers import Is_dec_int
from lexems_automats.sintaksis import *

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


def get_scanner_params():
    return file, lexema, row, base_position, offset


def seek_new_position():
    global base_position
    global offset

    file.seek(base_position)
    offset = 1


def tell_new_position():
    global base_position
    global offset

    base_position = file.tell()
    offset = 1


def get_next_lexema():

    global base_position
    global offset
    global row

    while True:  # while no stop char have been met
        char = file.read(1).lower()

        if is_eof(char):
            return 'EOF'

        if is_space(char):
            tell_new_position()
            return 'Space'

        if is_tab(char):
            tell_new_position()
            return 'Tab'

        if is_new_line(char):
            tell_new_position()
            row += 1
            return 'NewLine'
        """ if no split char was detected it means that the char is valuable and file position must be unset """
        file.seek(base_position)

        """ read inside automata """
        success, rests = Is_dec_int(get_scanner_params())
        if success:
            base_position += rests['offset']
            seek_new_position()
            return rests['lexeme']
        file.seek(base_position)

        success, rests = Is_id_or_kw(get_scanner_params())
        if success:
            base_position += rests['offset']
            seek_new_position()
            return rests['lexeme']
        file.seek(base_position)

        char = file.read(1).lower()
        if is_comma(char):
            return 'Comma'
        if is_colon(char):
            return 'Colon'
        if is_semicolon(char):
            return 'Semicolon'
        file.seek(base_position)

while True:
    if not lexema == 'EOF':
        lexema = get_next_lexema()
        print_lexeme(row, lexema)
    else:
        break

print('====== Scanning has been finished ======')
