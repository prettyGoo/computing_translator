__author__ = 'Nikita'

import lexems_automats.key_words

from lexems_automats.base import is_digit, is_hex_digit, is_letter

from value_detector import get_detected_value


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
        value = get_detected_value(file, base_position, local_offset)
        for _, function in lexems_automats.key_words.__dict__.items():
            if callable(function):
                success, rest = function(value)
                if success:
                    local_lexeme = rest
                    value = local_lexeme.lower()
                    break
        return True, {'lexeme': local_lexeme, 'offset': local_offset, 'value': value}
    else:
        file.seek(base_position)
        return False, None

