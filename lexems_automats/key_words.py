__author__ = 'Nikita'


def is_kw_write(chars):
    lexeme = 'Write'
    return chars == lexeme, lexeme


def is_kw_read(chars):
    lexeme = 'Read'
    return chars == lexeme, lexeme


def is_kw_end(chars):
    lexeme = 'End'
    return chars == lexeme, lexeme


def is_kw_goto(chars):
    lexeme = 'Goto'
    return chars == lexeme, lexeme


def is_kw_while(chars):
    lexeme = 'While'
    return chars == lexeme, lexeme


def is_kw_loop(chars):
    lexeme = 'Loop'
    return chars == lexeme, lexeme


def is_kw_do(chars):
    lexeme = 'Do'
    return chars == lexeme, lexeme
