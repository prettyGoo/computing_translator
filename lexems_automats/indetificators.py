__author__ = 'Nikita'

import lexems_automats.key_words

from lexems_automats.base import is_digit, is_hex_digit, is_letter


def Is_id_or_kw(scanner_params):
    file, _, _, base_position, offset = scanner_params

    local_lexeme = ''
    local_offset = 0

    char = file.read(1)
    local_offset += 1
    if is_letter(char):
        while True:
            char = file.read(1).lower()
            if is_digit(char) or is_letter(char):
                local_offset += 1
                continue
            else:
                local_lexeme = 'Id'
                break

        # checks if it is really Id or KeyWord
        file.seek(base_position)
        chars = file.read(local_offset).lower()
        for _, function in lexems_automats.key_words.__dict__.items():
            if callable(function):
                success, rest = function(chars)
                if success:
                    local_lexeme = rest
                    break
        return True, {'offset': local_offset, 'lexeme': local_lexeme}
    else:
        file.seek(base_position)
        return False, {}

