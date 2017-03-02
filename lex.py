__author__ = 'Nikita'

from scanner.sintaksis import *
from scanner.key_words import *  # TODO ADD ALL KEY WORDS
from scanner.numbers import *   # TODO UPDATE PREFIXES FOR INT FORMS


def print_lexema(row, lex, val):
    print('{}   lex:{}  val:{}'.format(row, lex, val))


def error_handler(buffer):
    print('{}   lex:{}  val:{}'.format(current_row, 'Error', buffer))


def work_with_buffer(buffer):
    if is_kw_write(buffer):
        print_lexema(current_row, 'Write', 'write')
    elif is_kw_read(buffer):
        print_lexema(current_row, 'Read', buffer)
    elif is_kw_end(buffer):
        print_lexema(current_row, 'End', 'end')
    # INTEGERS
    elif is_dec_int(buffer) or is_bin_int(buffer) or is_oct_int(buffer) or is_hex_int(buffer):
        print_lexema(current_row, 'Int', buffer)
    # REAL
    elif is_real(buffer):
        print_lexema(current_row, 'Real', buffer)
    # ID
    elif is_id(buffer):
        print_lexema(current_row, 'Id', buffer)
    elif is_space(buffer):
        return
    else:
        error_handler(buffer)

current_row = 1
buffer = ''


test_numbers = '1 12 d12 b11 b22 c77 c88 h1a\x03'
test_real = '12e1 12e+3 12e-3 12. 12.3 12.e1 12.3e1 12.3e+3 12.3e-3 .12 .12e1 .12e+3 .12e-3\x10.e+ 12.3e 12.3e- 12.e3+\x03'


line = test_real
separators = {'space': ' ', 'tab': '\x09', 'new_line': '\x10', 'eot': '\x03'}
for symbol in line:
    if symbol in separators.values():
        work_with_buffer(buffer)
        buffer = ''
        if symbol == '\n':
            current_row += 1
    else:
        buffer += symbol
