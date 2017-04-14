__author__ = 'Nikita'

import sys


def print_lexeme(row, lexeme, value):
    if lexeme:
        print('{}\tlex:{}\tval:{}'.format(row, lexeme, value))
    else:
        print('ERROR: empty lexeme or None')
        sys.exit(0)

# def print_lexeme(row, lexeme, value):
#     if lexeme == 'Real' or lexeme == 'Int':
#         print_typed_lexeme(row, lexeme,  value)
#     elif lexeme:
#         print_typeless_lexeme(row, lexeme, value)
#     else:
#         print('ERROR: LEXEME IS NONE OR EMPTY')
#         sys.exit(0)


# def print_typed_lexeme(row, lexeme,  value):
#     if lexeme == 'Real':
#         print('{}\tlex:{}\treal:{}\tval:{}'.format(row, lexeme, value, value))
#     elif lexeme == 'Int':
#         print('{}\tlex:{}\tint:{}\tval:{}'.format(row, lexeme, value, value))
#
#
# def print_typeless_lexeme(row, lexeme, value):
#     print('{}\tlex:{}\tval:{}'.format(row, lexeme, value))