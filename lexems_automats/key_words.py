__author__ = 'Nikita'

import scanner.sintaksis
import re

# TODO Numbers and IDS
def is_digit(ch):
    return '0' <= ch <= '9'


def is_id(ch):
    return 'a' <= ch.lower() <= 'z'  # TODO replace for abc1


# TODO Keywords
# def is_kw_write(ch):
#     return ch.lower() == 'write'
	
def is_kw_write(chars):
    return chars == 'write'





def is_kw_read(ch):
    return ch.lower() == 'read'


def is_kw_end(ch):
    return ch.lower() == 'end'


def is_kw_goto(ch):
    return ch.lower() == 'goto'


# LOOPS
def is_kw_while(ch):
    return ch.lower() == 'while'


def is_kw_loop(ch):
    return ch.lower() == 'loop'


def is_kw_do(ch):
    return ch.lower() == 'do'