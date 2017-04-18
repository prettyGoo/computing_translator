__author__ = 'Nikita'


def is_kw_write(chars):
    return chars == 'write', 'Write'


def is_kw_read(chars):
    return chars == 'read', 'Read'


def is_kw_beg(chars):
    return chars == 'begin', 'Begin'


def is_kw_end(chars):
    return chars == 'end', 'End'


def is_kw_mod(chars):
    return chars == 'mod', 'Mod'


def is_kw_if(chars):
    return chars == 'if', 'If'


def is_kw_case(chars):
    return chars == 'case', 'Case'


def is_kw_then(chars):
    return chars == 'then', 'Then'


def is_kw_else(chars):
    return chars == 'else', 'Else'


def is_kw_of(chars):
    return chars == 'of', 'Of'


def is_kw_or(chars):
    return chars == 'or', 'Or'


def is_kw_break(chars):
    return chars == 'break', 'Break'


def is_kw_goto(chars):
    return chars == 'goto', 'Goto'


def is_kw_while(chars):
    return chars == 'while', 'While'


def is_kw_loop(chars):
    return chars == 'loop', 'Loop'


def is_kw_do(chars):
    return chars == 'do', 'Do'


def is_kw_var(chars):
    return  chars == 'var', 'Var'


def is_kw_proc(chars):
    return chars == 'proc', 'Proc'


def is_kw_tools(chars):
    return chars == 'tools', 'Tools'


def is_kw_call(chars):
    return chars == 'call', 'Call'


def is_kw_cast(chars):
    return chars == 'cast', 'Cast'
