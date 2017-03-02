__author__ = 'Nikita'

from scanner.sintaksis import *
from scanner.key_words import *
from scanner.numbers import *


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
    # ID
    elif is_id(buffer):
        print_lexema(current_row, 'Id', buffer)
    elif is_space(buffer):
        return
    else:
        error_handler(buffer)

current_row = 1
buffer = ''

line = 'b011 c122 Ha 12\x03'
separators = {'space': ' ', 'tab': '\x09', 'new_line': '\x10', 'eot': '\x03'}
for symbol in line:
    if symbol in separators.values():
        work_with_buffer(buffer)
        buffer = ''
        if symbol == '\n':
            current_row += 1
    else:
        buffer += symbol
