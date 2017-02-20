__author__ = 'Nikita'

import os
import sys


def is_digit(ch):
    return '0' <= ch <= '9'


def is_space(ch):
    return ch == ' '


def is_kw_write(ch):
    return ch.lower() == 'write'


def printer(row, lex, val):
    print('{}   lex:{}  val:{}'.format(row, lex, val))


def string_former(line, current_column, shift):
    s = ''
    for i in range(shift+1):
        s += line[current_column-1+i]
    return s

if __name__ == '__main__':
    line = input('Write line: ')
    # line2 = input('Write line: ')
    # line = line1 + line2
    current_row = 1
    current_column = 1
    shift = 0
    # for line in lines:
    while current_column + shift <= len(line):
        ch = string_former(line, current_column, shift)
        if is_kw_write(ch):
            printer(current_row, 'Write', 'write')
            current_column, shift = current_column + shift + 1, 0
            continue
        elif is_digit(ch):
            printer(current_row, 'Int', ch)
            current_column, shift = current_column + shift + 1, 0
            continue
        elif is_space(ch):
            printer(current_row, 'Space', ch)
            current_column, shift = current_column + shift + 1, 0
            continue
        shift += 1
    # shift = 0
    # current_row += 1