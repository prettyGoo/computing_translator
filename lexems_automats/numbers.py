__author__ = 'Nikita'

import re

from lexems_automats.base import is_digit, is_bin_digit, is_oct_digit, is_hex_digit
from lexems_automats.base import is_letter

from lexems_automats.sintaksis import *

from value_detector import get_detected_value


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

        if not (is_letter(char) or is_digit(char)):
            return True, {'lexeme': 'Int', 'offset': local_offset, 'value': value}
        else:
            if is_hex_digit(char) or char == 'h':
                return False, None
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

        if not (is_letter(char) or is_digit(char) or is_colon(char)):
            return True, {'lexeme': 'Int', 'offset': local_offset, 'value': value}
        else:
            if is_hex_digit(char) or char == 'h':
                return False, None
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

        if not (is_letter(char) or is_digit(char) or is_colon(char)):
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
            lexeme_is_formed, local_offset = is_exponenta(file, local_offset)

            local_offset -= 1
            value = get_detected_value(file, base_position, local_offset)
            if lexeme_is_formed:
                char = file.read(1).lower()
                if not (is_letter(char) or char == '.'):
                    return True, {'lexeme': 'Real', 'offset': local_offset, 'value': value}
                else:
                    return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': value+char}
            else:
                char = file.read(1).lower()
                if is_hex_digit(char) or char == 'h':
                    return False, None
                else:
                    return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': value}
        elif char == '.':
            char = file.read(1).lower()
            local_offset += 1
            if is_digit(char):
                while is_digit(char):
                    char = file.read(1).lower()
                    local_offset += 1

            if char == 'e':
                lexeme_is_formed, local_offset = is_exponenta(file, local_offset)

                local_offset -= 1
                value = get_detected_value(file, base_position, local_offset)
                if lexeme_is_formed:
                    char = file.read(1).lower()
                    if not (is_letter(char) or char == '.'):
                        return True, {'lexeme': 'Real', 'offset': local_offset, 'value': value}
                    else:
                        return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': value+char}
                else:
                    return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': value}
            else:
                local_offset -= 1
                file.seek(base_position)
                chars = file.read(local_offset).lower()
                char = file.read(1).lower()
                if not (is_letter(char) or char == '.'):
                    return True, {'lexeme': 'Real', 'offset': local_offset, 'value': chars}
                else:
                    return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': chars+char}

    elif char == '.':
        char = file.read(1).lower()
        local_offset += 1
        if is_digit(char):
            while is_digit(char):
                char = file.read(1).lower()
                local_offset += 1

            if char == 'e':
                lexeme_is_formed, local_offset = is_exponenta(file, local_offset)

                local_offset -= 1
                value = get_detected_value(file, base_position, local_offset)
                if lexeme_is_formed:
                    char = file.read(1).lower()
                    if not (is_letter(char) or char == '.'):
                        return True, {'lexeme': 'Real', 'offset': local_offset, 'value': value}
                    else:
                        return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': value+char}
                else:
                    return False, {'lexeme': 'Error', 'error': 'Real number form', 'value': value}
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


def is_exponenta(file, offset):
    char = file.read(1).lower()
    offset += 1

    sign_is_stop = False
    digit_is_present = False
    while is_digit(char) or (char in '+-' and not sign_is_stop and not digit_is_present):
        if char in '+-':
            sign_is_stop = True
        if is_digit(char):
            digit_is_present = True
        char = file.read(1).lower()
        offset += 1

    if digit_is_present:
        return True, offset
    else:
        return False, offset