__author__ = 'Nikita'


def print_lexeme(row, lexeme, value=None):
    if lexeme:
        if value:
            print('{}\tlex:{}\tval:{}'.format(row, lexeme, value))
        else:
            print('{}\tlex:{}\tval:{}'.format(row, lexeme, lexeme.lower()))
