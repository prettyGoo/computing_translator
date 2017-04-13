__author__ = 'Nikita'

from lexems_automats.base import is_digit, is_bin_digit, is_oct_digit, is_hex_digit
from lexems_automats.base import is_letter


def Is_bin_int(scaner_maras):
    file, _, _, _, _ = scaner_maras

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


def Is_dec_int(scanner_params):
    file, _, _, _, _ = scanner_params

    char = file.read(1)
    local_offset = 1
    if is_digit(char):
        while True:
            char = file.read(1)
            if not is_digit(char):
                if char == 'd':
                    local_offset += 1
                break
            else:
                local_offset += 1
        if not (is_letter(char) and is_digit(char)):
            return True, {'offset': local_offset, 'lexeme': 'DecInt'}
        else:
            return False, {'error': "Dec integer's form is wrong"}
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
