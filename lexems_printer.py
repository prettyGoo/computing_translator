__author__ = 'Nikita'

import sys


def print_lexeme(row, lexeme, value):
    if lexeme:
        if lexeme == 'Real':
            print('{}\tlex:{}\treal:{}\tval:{}'.format(row, lexeme, value, float(value)))
        elif lexeme == 'Int':
            digit_base = value[-1]
            if digit_base == 'b':
                digit_base = 2
            elif digit_base == 'c':
                digit_base = 8
            elif digit_base == 'd':
                digit_base = 10
            elif digit_base == 'h':
                digit_base = 16
            number = value[:len(value)-1]
            print('{}\tlex:{}\tint:{}\tval:{}'.format(row, lexeme, value, int(number, digit_base)))
        else:
            print('{}\tlex:{}\tval:{}'.format(row, lexeme, value))
    else:
        print('ERROR: empty lexeme or None')
        sys.exit(0)