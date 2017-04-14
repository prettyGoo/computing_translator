__author__ = 'Nikita'

import re

from lexems_automats.base import is_digit, is_bin_digit, is_oct_digit, is_hex_digit
from lexems_automats.base import is_letter

from lexems_automats.sintaksis import is_split, is_colon


def Is_bin_int(scaner_params):
    file, _, _, _, _ = scaner_params

    char = file.read(1)
    local_offset = 1
    if is_bin_digit(char):
        while True:
            char = file.read(1).lower()
            if not is_bin_digit(char):
                if char == 'b':
                    local_offset += 1
                    break
                else:
                    return False, {'error': "Bin integer's form is wrong"}
            local_offset += 1
        char = file.read(1)
        if not (is_letter(char) and is_digit(char)):
            return True, {'offset': local_offset, 'lexeme': 'BinInt'}
        else:
            return False, {'error': "Bin integer's form is wrong"}
    else:
        return False, {}


def Is_oct_int(scanner_params):
    file, _, _, _, _ = scanner_params

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
                    return False, {'error': "Oct integer's form is wrong"}
            local_offset += 1
        char = file.read(1)
        if not (is_letter(char) and is_digit(char)):
            return True, {'offset': local_offset, 'lexeme': 'OctInt'}
        else:
            return False, {'error': "OctInt integer's form is wrong"}
    else:
        return False, {}


def Is_dec_int_or_label(scanner_params):
    file, _, _, _, _ = scanner_params
    local_lexeme = ''

    char = file.read(1)
    local_offset = 1
    if is_digit(char):
        while True:
            char = file.read(1)
            if not is_digit(char):
                if char == 'd':  # it is still dec integer
                    local_offset += 1
                    local_lexeme = 'DecInt'
                elif is_colon(char):  # it is a label
                    local_offset += 1
                    local_lexeme = 'Label'
                break
            else:
                local_offset += 1

        char = file.read(1)
        if local_lexeme == 'DecInt' and not (is_letter(char) or is_digit(char)):
            return True, {'offset': local_offset, 'lexeme': local_lexeme}
        elif local_lexeme == 'Label' and is_split(char):
            return True, {'offset': local_offset, 'lexeme': local_lexeme}
        else:
            return False, {'error': "Dec integer's or label's forms are wrong"}
    else:
        return False, {}


def Is_hex_int(scanner_params):
    file, _, _, _, _ = scanner_params

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
                    return False, {'error': "Hex integer's form is wrong"}
            local_offset += 1
        char = file.read(1)
        if not (is_letter(char) and is_digit(char)):
            return True, {'offset': local_offset, 'lexeme': 'HexInt'}
        else:
            return False, {'error': "HexInt integer's form is wrong"}
    else:
        return False, {}


def Is_real(scanner_params):
    file, _, _, base_position, _ = scanner_params

    pattern_one = r'\d+e(\+|\-)?\d+$'
    pattern_two = r'\d+\.\d*(e(\+|\-)?\d+)?$'
    patter_three = r'\.\d+(e(\+|\-)?\d+)?$'

    first_char = file.read(1)
    local_offset = 1

    if is_digit(first_char) or first_char == '.':
        while True:
            char = file.read(1)
            if is_split(char):
                break
            local_offset += 1
        file.seek(base_position)
        chars = file.read(local_offset)
        if first_char == '.':
            if re.match(patter_three, chars):
                return True, {"offset": local_offset, 'lexeme': 'Real'}
        else:
            if re.match(pattern_one, chars) or re.match(pattern_two, chars):
                return True, {"offset": local_offset, 'lexeme': 'Real'}
        return False, {}
    else:
        return False, {}