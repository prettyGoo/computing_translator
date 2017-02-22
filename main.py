__author__ = 'Nikita'

import os
import sys

import scanner.scan as scanner


def print_lexema(row, lex, val):
    print('{}   lex:{}  val:{}'.format(row, lex, val))


def string_former(line, current_column, shift):
    s = ''
    for i in range(shift+1):
        s += line[current_column-1+i]
    return s


def line_slitter(line):
    """
    :param line:
    :return: list of
    """
    l = line.split(' ')
    for a in l:
        if len(a) == 1:
            print(ord(a))
    print(l)

if __name__ == '__main__':
    # line = input('Write line: ')
    line = 'write abc7 goto end 1 read'
    line = line.split(' ')  # TODO Make it valid for every splitter (comment, tab, space, new line)
    current_row = 1
    current_column = 1
    shift = 0

    while current_column + shift <= len(line):
        ch = string_former(line, current_column, shift)
        if scanner.is_kw_write(ch):
            print_lexema(current_row, 'Write', 'write')
            current_column, shift = current_column + shift + 1, 0
            continue
        elif scanner.is_digit(ch):
            print_lexema(current_row, 'Int', ch)
            current_column, shift = current_column + shift + 1, 0
            continue
        elif scanner.is_space(ch):
            print_lexema(current_row, 'Space', ch)
            current_column, shift = current_column + shift + 1, 0
            continue
        shift += 1
    # shift = 0
    # current_row += 1