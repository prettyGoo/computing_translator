import sys

from lexems_automats.indetificators import Is_id_or_kw
from lexems_automats.numbers import Is_dec_int_or_label, Is_bin_int, Is_oct_int, Is_hex_int, Is_real
from lexems_automats.math_operations import *
from lexems_automats.sintaksis import *

from lexems_printer import print_lexeme

try:
    file = open('code5.txt', 'r')
except FileNotFoundError:
    print('Aborted: the file you are looking for does not exist\n')
    sys.exit(0)

lexeme = 'NoLex'
row = 1
base_position = 0
offset = 1


def get_scanner_params():
    return file, lexeme, row, base_position, offset


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


def check_automat_output(success, rests):
    global base_position
    if success:
        base_position += rests['offset']
        seek_new_position()
        return rests['lexeme'], rests['value']
    elif rests:
        error_loop()
        return rests['lexeme'], rests['value']


def error_loop():
    # read chars while \n is not found
    # then when \n has been found, seek one position back
    global row
    while True:
        char = file.read(1)
        if is_new_line(char):
            file.seek(file.tell()-1)
            tell_new_position()
            break
        if is_eof(char):
            file.seek(file.tell())
            tell_new_position()
            break


def comment_loop():
    global row

    while True:
        char = file.read(1)
        if is_right_curly_bracket(char):
            return
        if is_new_line(char):
            row += 1
        if is_eof(char):
            print('Eof but comment has not been finished')
            sys.exit(0)


def get_next_lexema():

    global base_position
    global offset
    global row

    while True:  # while no stop char have been met
        char = file.read(1).lower()

        if is_eof(char):
            return 'EOF', 'eof'

        if is_left_curly_bracket(char):
            comment_loop()
            tell_new_position()
            return 'LCB', '{'
        if is_right_curly_bracket(char):
            tell_new_position()
            return 'RCB', '}'

        if is_space(char):
            tell_new_position()
            return 'Space', 'space'

        if is_tab(char):
            tell_new_position()
            return 'Tab', 'tab'

        if is_new_line(char):
            tell_new_position()
            row += 1
            return 'NewLine', 'newline'
        """ if no split char was detected it means that the char is valuable and file position must be unset """
        file.seek(base_position)

        """ read inside automata """
        status, rests = Is_real(get_scanner_params())
        result = check_automat_output(status, rests)
        if result:
            return result
        file.seek(base_position)

        status, rests = Is_bin_int(get_scanner_params())
        result = check_automat_output(status, rests)
        if result:
            return result
        file.seek(base_position)

        status, rests = Is_oct_int(get_scanner_params())
        result = check_automat_output(status, rests)
        if result:
            return result
        file.seek(base_position)

        status, rests = Is_hex_int(get_scanner_params())
        result = check_automat_output(status, rests)
        if result:
            return result
        file.seek(base_position)

        status, rests = Is_dec_int_or_label(get_scanner_params())
        result = check_automat_output(status, rests)
        if result:
            return result
        file.seek(base_position)

        status, rests = Is_id_or_kw(get_scanner_params())
        result = check_automat_output(status, rests)
        if result:
            return result
        file.seek(base_position)

        char = file.read(1).lower()
        if is_comma(char):
            tell_new_position()
            return 'Comma', ','
        if is_colon(char):
            tell_new_position()
            return 'Colon', ':'
        if is_semicolon(char):
            tell_new_position()
            return 'Semicolon', ';'

        if is_left_round_bracket(char):
            tell_new_position()
            return 'LRB', '('
        if is_right_round_bracket(char):
            tell_new_position()
            return 'RRB', ')'
        if is_left_square_bracket(char):
            tell_new_position()
            return 'LSB', '['
        if is_right_suqare_bracket(char):
            tell_new_position()
            return 'RSB', ']'

        if is_add(char):
            tell_new_position()
            return 'Add', '+'
        if is_min(char):
            tell_new_position()
            return 'Min', '-'
        if is_mul(char):
            tell_new_position()
            return 'Mul', '*'
        if is_div(char):
            tell_new_position()
            return 'Div', '/'

        chars = char + file.read(2)

        status, rests = Is_let(chars)
        result = check_automat_output(status, rests)
        if result:
            return result

        status, rests = Is_ne(chars)
        result = check_automat_output(status, rests)
        if result:
            return result

        status, rests = Is_le(chars)
        result = check_automat_output(status, rests)
        if result:
            return result

        status, rests = Is_ge(chars)
        result = check_automat_output(status, rests)
        if result:
            return result


        chars = chars[:len(chars)-1]
        if is_eq(chars):
            base_position += 1
            seek_new_position()
            return 'EQ', '='
        if is_lt(chars):
            base_position += 1
            seek_new_position()
            return 'LT', '<'
        if is_gt(chars):
            base_position += 1
            seek_new_position()
            return 'GT', '>'


while True:
    if not lexeme == 'EOF':
        lexeme, value = get_next_lexema()
        print_lexeme(row, lexeme, value)
    else:
        break

print('====== Scanning has been finished ======')
