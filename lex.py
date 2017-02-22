__author__ = 'Nikita'

from scanner.scan import *


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
    elif is_id(buffer):
        print_lexema(current_row, 'Id', buffer)
    # elif is_digit(buffer):
    #     print_lexema(current_row, 'Digit', buffer)
    elif is_space(buffer):
        return
    else:
        error_handler(buffer)

current_row = 1
buffer = ''

line = 'write\n7abc ! end read\n'
separators = {'space': ' ', 'tab': '    ', 'new_line': '\n'}
for symbol in line:
    if symbol in separators.values():
        work_with_buffer(buffer)
        buffer = ''
        current_row = current_row + 1 if symbol == '\n' else current_row
    else:
        buffer += symbol
