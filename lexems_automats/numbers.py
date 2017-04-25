__author__ = 'Nikita'

import re

from lexems_automats.base import is_digit, is_bin_digit, is_oct_digit, is_hex_digit
from lexems_automats.base import is_letter

from lexems_automats.sintaksis import *

from value_detector import get_detected_value

max_float = 1.701411733e+38


def Is_bin_int(scaner_params):
    file, _, _, base_position, _ = scaner_params

    char = file.read(1).lower()
    local_offset = 1
    if is_bin_digit(char):
        while True:
            char = file.read(1).lower()
            if not is_bin_digit(char):
                if char == 'b':
                    local_offset += 1
                    break
                else:
                    return False, None
            local_offset += 1

        char = file.read(1).lower()
        value = get_detected_value(file, base_position, local_offset)

        if not (is_letter(char) and is_digit(char)):
            return True, {'lexeme': 'Int', 'offset': local_offset, 'value': value}
        else:
            return False, {'lexeme': 'Error', 'error': "Bin integer's form is wrong", 'value': value + char}
    else:
        return False, None


def Is_oct_int(scanner_params):
    file, _, _, base_position, _ = scanner_params

    char = file.read(1).lower()
    local_offset = 1
    if is_oct_digit(char):
        while True:
            char = file.read(1).lower()
            if not is_oct_digit(char):
                if char == 'c':
                    local_offset += 1
                    break
                else:
                    return False, None
            local_offset += 1

        char = file.read(1).lower()
        value = get_detected_value(file, base_position, local_offset)

        if not (is_letter(char) and is_digit(char)):
            return True, {'lexeme': 'Int', 'offset': local_offset, 'value': value}
        else:
            return False, {'lexeme': 'Error', 'error': "OctInt integer's form is wrong",'value': value + char}
    else:
        return False, None


def Is_hex_int(scanner_params):
    file, _, _, base_position, _ = scanner_params

    char = file.read(1).lower()
    local_offset = 1
    if is_hex_digit(char):
        while True:
            char = file.read(1).lower()
            if not is_hex_digit(char):
                if char == 'h':
                    local_offset += 1
                    break
                else:
                    return False, None
            local_offset += 1

        char = file.read(1).lower()
        value = get_detected_value(file, base_position, local_offset)

        if not (is_letter(char) and is_digit(char)):
            return True, {'lexeme': 'Int', 'offset': local_offset, 'value': value}
        else:
            return False, {'lexeme': 'Error', 'error': "HexInt integer's form is wrong", 'value': value + char}
    else:
        return False, None


def Is_dec_int_or_label(scanner_params):
    file, _, _, base_position, _ = scanner_params
    local_lexeme = ''

    char = file.read(1).lower()
    local_offset = 1
    if is_digit(char):
        local_lexeme = 'Int'
        while True:
            char = file.read(1).lower()
            if not is_digit(char):
                if char == 'd':  # it is still dec integer
                    local_offset += 1
                elif is_colon(char):  # it is a label
                    local_offset += 1
                    local_lexeme = 'Label'
                file.seek(base_position+local_offset)
                break
            else:
                local_offset += 1

        afterchar = file.read(1).lower() if not is_new_line(char) else ''
        value = get_detected_value(file, base_position, local_offset)

        if local_lexeme == 'Int' and not (is_letter(afterchar) or is_digit(afterchar)) \
           or local_lexeme == 'Label' and is_split(afterchar):
                return True, {'lexeme': local_lexeme, 'offset': local_offset, 'value': value}
        else:
            return False, {'lexeme': 'Error', 'error': "Dec integer's or label's forms are wrong", 'value': value + char}
    else:
        return False, None


def Is_real(scanner_params):
    file, _, _, base_position, _ = scanner_params


    char = file.read(1).lower()
    local_offset = 1
    lexeme_is_formed = False

    if is_digit(char):
        while is_digit(char):
            char = file.read(1).lower()
            local_offset += 1
        if char == 'e':
            char = file.read(1).lower()
            local_offset += 1

            sign_is_stop = False
            digit_is_present = False
            while is_digit(char) or (char in '+-' and not sign_is_stop and not digit_is_present):
                if char in '+-':
                    sign_is_stop = True
                if is_digit(char):
                    digit_is_present = True
                char = file.read(1).lower()
                local_offset += 1

            if digit_is_present:
                lexeme_is_formed = True

            local_offset -= 1
            file.seek(base_position)
            chars = file.read(local_offset)
            if lexeme_is_formed:
                char = file.read(1)
                if not (is_letter(char) or char == '.'):
                    return True, {'lexeme': 'Real', 'offset': local_offset, 'value': chars}
                else:
                    return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': chars+char}
            else:
                return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': chars}

        elif char == '.':
            char = file.read(1).lower()
            local_offset += 1
            if is_digit(char):
                while is_digit(char):
                    char = file.read(1)
                    local_offset += 1

            if char == 'e':
                char = file.read(1).lower()
                local_offset += 1

                sign_is_stop = False
                digit_is_present = False
                while is_digit(char) or (char in '+-' and not sign_is_stop and not digit_is_present):
                    if char in '+-':
                        sign_is_stop = True
                    if is_digit(char):
                        digit_is_present = True
                    char = file.read(1).lower()
                    local_offset += 1

                if digit_is_present:
                    lexeme_is_formed = True

                local_offset -= 1
                file.seek(base_position)
                chars = file.read(local_offset)
                if lexeme_is_formed:
                    char = file.read(1)
                    if not (is_letter(char) or char == '.'):
                        return True, {'lexeme': 'Real', 'offset': local_offset, 'value': chars}
                    else:
                        return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': chars+char}
                else:
                    return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': chars}
            else:
                local_offset -= 1
                file.seek(base_position)
                chars = file.read(local_offset)
                char = file.read(1)
                if not (is_letter(char) or char == '.'):
                    return True, {'lexeme': 'Real', 'offset': local_offset, 'value': chars}
                else:
                    return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': chars+char}

    elif char == '.':
        char = file.read(1)
        local_offset += 1
        if is_digit(char):
            while is_digit(char):
                char = file.read(1)
                local_offset += 1

            if char == 'e':
                char = file.read(1).lower()
                local_offset += 1

                sign_is_stop = False
                digit_is_present = False
                while is_digit(char) or (char in '+-' and not sign_is_stop and not digit_is_present):
                    if char in '+-':
                        sign_is_stop = True
                    if is_digit(char):
                        digit_is_present = True
                    char = file.read(1).lower()
                    local_offset += 1

                if digit_is_present:
                    lexeme_is_formed = True

                local_offset -= 1
                file.seek(base_position)
                chars = file.read(local_offset)
                if lexeme_is_formed:
                    char = file.read(1)
                    if not (is_letter(char) or char == '.'):
                        return True, {'lexeme': 'Real', 'offset': local_offset, 'value': chars}
                    else:
                        return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': chars+char}
                else:
                    return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': chars}
            elif is_letter(char):
                value = get_detected_value(file, base_position, local_offset)
                return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': value}
            else:
                local_offset -= 1
                value = get_detected_value(file, base_position, local_offset)
                return True, {'lexeme': 'Real', 'offset': local_offset, 'value': value}
        else:
            return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': '.'+char}
    else:
        return False, None

    return False, None


# old
# def Is_real_last(scanner_params):
#     file, _, _, base_position, _ = scanner_params
#
#     pattern_one = r'\d+e(\+|\-)?\d+$'
#     pattern_two = r'\d+\.\d*(e(\+|\-)?\d+)?$'
#     patter_three = r'\.\d+(e(\+|\-)?\d+)?$'
#
#     char = file.read(1)
#     first_char = char
#     local_offset = 1
#     buf = char
#
#     if is_digit(char) or char == '.':
#         while True:  # we cannot do match firstly, since 11e+11 will fire 11e+1
#             if is_digit(char) or char == '+' or char == '-' or char == 'e' or char == '.':
#                 char = file.read(1)
#                 local_offset += 1
#             else:
#                 break
#
#         local_offset, loop_offset = 1, local_offset
#         once_passed = False
#         point_passed = False
#
#         for i in range(loop_offset):
#             file.seek(base_position)
#             chars = file.read(local_offset)
#             if (re.match(patter_three, chars) or re.match(pattern_one, chars) or re.match(pattern_two, chars)) and not once_passed and not is_new_line(list(chars)[-1]):
#                 if first_char == '.':
#                     if point_passed:
#                         once_passed = True
#                     else:
#                         point_passed = True
#                 else:
#                     once_passed = True
#
#             if (not(re.match(patter_three, chars) or re.match(pattern_one, chars) or re.match(pattern_two, chars)) and once_passed) \
#                     or (is_new_line(list(chars)[-1]) and once_passed):
#                 if not is_letter(char):
#                     if not is_split(char):
#                         return True, {'lexeme': 'Real', 'offset': local_offset-1, 'value': ''.join(chars.split())[:-1]}
#                     else:
#                         return True, {'lexeme': 'Real', 'offset': local_offset-1, 'value': chars[:len(chars)-1]}
#                 else:
#                     return False, {'lexeme': 'Error', 'error': "Real number's form is wrong", 'value': chars + char}
#             local_offset += 1
#         return False, None
#     else:
#         next_char = file.read(1)
#         if char == 'e' and is_digit(next_char):
#             return False, {'lexeme': 'Error', 'error': 'Lexemes confusion', 'value': 'e' + next_char}
#         return False, None


# def Is_Real(scanner_params):
#     file, _, _, base_position, _ = scanner_params
#
#     pattern_one = r'\d+e(\+|\-)?\d+$'
#     pattern_two = r'\d+\.\d*(e(\+|\-)?\d+)?$'
#     patter_three = r'\.\d+(e(\+|\-)?\d+)?$'
#
#     char = file.read(1)
#     local_offset = 1
#     buf = char
#     if is_digit(char) or char == '.':
#         while True:  # we cannot do match firstly, since 11e+11 will fire 11e+1
#             if is_digit(char) or char == '+' or char == '-' or char == 'e' or char == '.':
#                 char = file.read(1)
#                 buf += char
#                 local_offset += 1
#             else:
#                 buf = buf[:-1]
#                 break
#
#         local_offset, loop_offset = 1, local_offset
#         once_passed = False
#         # since 11e+11 will fire 11e+1, additional check:; it may be correct 11e+1 or 11e+1+1 which is three lexemes
#         for i in range(loop_offset):  # additional check since it may be correct 11e+1 or 11e+1+1 which is three lexemes
#             file.seek(base_position)
#             chars = file.read(local_offset)
#             if (re.match(patter_three, chars) or re.match(pattern_one, chars) or re.match(pattern_two, chars)) and not once_passed and not is_new_line(list(chars)[-1]):
#                 once_passed = True
#             if (not(re.match(patter_three, chars) or re.match(pattern_one, chars) or re.match(pattern_two, chars)) and once_passed) \
#                     or (is_new_line(list(chars)[-1]) and once_passed):
#                 if not is_letter(char):
#                     if not wrong_exponenta(buf):
#                         if not is_split(char):
#                             return True, {'lexeme': 'Real', 'offset': local_offset-1, 'value': ''.join(chars.split())[:-1]}
#                         else:
#                             return True, {'lexeme': 'Real', 'offset': local_offset-1, 'value': chars[:len(chars)-1]}
#                     else:
#                         return False, {'lexeme': 'Error', 'error': "Real number's form is wrong", 'value': buf}
#                 else:
#                     return False, {'lexeme': 'Error', 'error': "Real number's form is wrong", 'value': chars + char}
#             local_offset += 1
#         return False, None
#     else:
#         next_char = file.read(1)
#         if char == 'e' and is_digit(next_char):
#             return False, {'lexeme': 'Error', 'error': 'Lexemes confusion', 'value': 'e' + next_char}
#         return False, None


# def Is_real_old(scanner_params):
#     file, _, _, base_position, _ = scanner_params
#
#     must_meet = '.e'
#     can_meet = '.+-e'
#     cannot_meet = ''
#
#
#     pattern_one = r'\d+e(\+|\-)?\d+$'
#     pattern_two = r'\d+\.\d*(e(\+|\-)?\d+)?$'
#     patter_three = r'\.\d+(e(\+|\-)?\d+)?$'
#
#     char = file.read(1).lower()
#     local_offset = 1
#     if is_digit(char) or char == '.':
#         while True:  # we cannot do match firstly, since 11e+11 will fire 11e+1
#             if is_digit(char) or char == '+' or char == '-' or char == 'e' or char == '.':
#                 char = file.read(1).lower()
#                 local_offset += 1
#             else:
#                 break
#
#         file.seek(base_position)
#         chars = file.read(local_offset)
#
#         for i, char in enumerate(chars):
#             if char in must_meet:
#                 must_meet = ''
#
#             if char == '.':
#                 if char in cannot_meet:
#                     return False, {'lexeme': 'Error', 'error': "Real number's form is wrong", 'value': chars}
#                 if not is_digit(char[i + 1]):
#                     return False, {'lexeme': 'Error', 'error': "Real number's form is wrong", 'value': chars}
#                 can_meet.replace(char, '')
#                 cannot_meet += char
#
#             if char == 'e':
#                 if char in cannot_meet:
#                     return False, {'lexeme': 'Error', 'error': "Real number's form is wrong", 'value': chars}
#                 if not ((char[i+1] == 'e' and is_digit(char[i+2])) and ((char[i+1] != 'e' and is_digit(char[i+1])) )):
#                     return False, {'lexeme': 'Error', 'error': "Real number's form is wrong", 'value': chars}
#                 can_meet.replace(char, '')
#                 cannot_meet += char
#
#             if char == '+' or char == '-':
#                 if i == 0:
#                     return False, None
#                 if char in cannot_meet:
#                     return False, {'lexeme': 'Error', 'error': "Real number's form is wrong", 'value': chars }
#                 if char[i-1] != 'e':
#                     return False, {'lexeme': 'Error', 'error': "Real number's form is wrong", 'value': chars}
#                 if not is_digit(char[i+1]):
#                     return False, {'lexeme': 'Error', 'error': "Real number's form is wrong", 'value': chars}
#                 can_meet.replace(char, '')
#                 cannot_meet += char
#
#         return False, None
#
#     return False, None
#
#
def wrong_exponenta(e):
    return e in ['..', '.', '..1', '1..', '1ee1', 'e1', '.e10', '11e11e11', '11.11.11', '1e-1']