import sys

from lexems_automats.base import is_digit, is_hex_digit, is_letter
from lexems_automats.indetificators import Is_id_or_kw
from lexems_automats.numbers import Is_dec_int
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


def get_scanner_params():
    global lexema
    global row
    global base_position
    global offset

    return file, lexema, row, base_position, offset


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

    file.seek(base_position)
    offset = 1


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
        success, rest = Is_dec_int(get_scanner_params())
        if success:
            base_position += rest['offset']
            seek_new_position()
            return rest['lexeme']
        file.seek(base_position)

        success, rest = Is_id_or_kw(get_scanner_params())
        if success:
            base_position += rest['offset']
            seek_new_position()
            return rest['lexeme']
        file.seek(base_position)


while True:
    if not lexema == 'EOF':
        lexema = get_next_lexema()
        print_lexeme(row, lexema)
    else:
        break

print('====== Scanning has been finished ======')
