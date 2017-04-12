__author__ = 'Nikita'

import sys

from scanner.sintaksis import *
from scanner.key_words import *  # TODO ADD ALL KEY WORDS
from scanner.numbers import *   # TODO UPDATE PREFIXES FOR INT FORMS


def print_lexema(row, lex, val):
    print('{}   lex:{}  val:{}'.format(row, lex, val))


def error_handler(buffer):
    print('{}   lex:{}  val:{}'.format(current_row, 'Error', buffer))


def work_with_buffer(buffer):
    # KEYWORDS
    if is_kw_write(buffer):
        print_lexema(current_row, 'Write', 'write')
    elif is_kw_read(buffer):
        print_lexema(current_row, 'Read', buffer)
    elif is_kw_end(buffer):
        print_lexema(current_row, 'End', 'end')
    # OPERATORS
    # INTEGERS
    elif is_dec_int(buffer) or is_bin_int(buffer) or is_oct_int(buffer) or is_hex_int(buffer):
        print_lexema(current_row, 'Int', buffer)
    # REAL
    elif is_real(buffer):
        print_lexema(current_row, 'Real', buffer)
    # ID
    elif is_id(buffer):
        print_lexema(current_row, 'Id', buffer)
    # SINTAKSIS
    elif is_space(buffer):
        return
    # ERROR
    else:
        error_handler(buffer)

current_row = 1
buffer = ''


test_numbers = '1 12 d12 b11 b22 c77 c88 h1a\x03'
test_real = '12e1 12e+3 12e-3 12. 12.3 12.e1 12.3e1 12.3e+3 12.3e-3 .12 .12e1 .12e+3 .12e-3\x10.e+ 12.3e 12.3e- 12.e3+\x03'


line = test_real
separators = {'space': ' ', 'tab': '\x09', 'new_line': '\x10', 'eot': '\x03'}




try:
    file = open('code.txt', 'r')
except FileNotFoundError:
    print('Aborted: the file you are looking for does not exist\n')
    sys.exit(0)

line = 1
base_column = file.tell()
offset = base_column + 1


def unset():
    file.seek(base_column)
    offset = base_column + 1


def next_symbol():
    return file.read(1)



#lexema
#
while True {
    lexema = 
}




for _ in range(30):
    chars_buffer = file.read(offset-from_what) # if there is nothing to read - EOF - read() returns the string of lenght 0

    # next_automata = False

    # 1 - true, 0 - not know, -1 - false
    while True:
        if is_kw_write(buffer) == 1:
            print_lexema(buffer, 'Write', 'write')
        elif is_kw_write(buffer) == 0:
            offset += 1
            buffer = file.read(offset-from_what)
        elif is_kw_write(buffer) == -1:
            offset = from_what + 1
            break

    # is_kw_write(read_string):
    #     print_lexema(current_row, 'Write', 'write')
    # elif is_kw_read(read_string):
    #     print_lexema(current_row, 'Read', buffer)

    # if len(read_string) == 0:
    #     print('EOF')
    #     break

    # from_what = offset

# for symbol in line:
#     if symbol in separators.values():
#         work_with_buffer(buffer)
#         buffer = ''
#         if symbol == '\n':
#             current_row += 1
#     else:
#         buffer += symbol
