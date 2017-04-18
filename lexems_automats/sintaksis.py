__author__ = 'Nikita'


def is_eof(ch):
    return not ch


def is_space(ch):
    return ch == ' '


def is_tab(ch):
    return ch == '\t'


def is_new_line(ch):
    return ch == '\n'


def is_split(ch):
    return is_space(ch) or is_tab(ch) or is_new_line(ch) or is_eof(ch)


def is_comma(ch):
    return ch == ','


def is_colon(ch):
    return ch == ':'


def is_semicolon(ch):
    return ch == ';'


def is_left_curly_bracket(char):
    return char == '{'


def is_right_curly_bracket(char):
    return char == '}'


def is_left_round_bracket(char):
    return char == '('


def is_right_round_bracket(char):
    return char == ')'


def is_left_square_bracket(char):
    return char == '['


def is_right_suqare_bracket(char):
    return char == ']'


def is_punctuation(ch):
    return is_comma(ch) or is_colon(ch) or is_semicolon(ch) or is_left_curly_bracket(ch)
