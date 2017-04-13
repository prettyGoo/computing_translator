__author__ = 'Nikita'

from lexems_automats.base import is_digit, is_hex_digit, is_letter


def Is_dec_int(scanner_params):

    file, _, _, _, _ = scanner_params

    local_offset = 1
    char = file.read(1)
    if is_digit(char):
        while True:
            char = file.read(1)
            if is_digit(char):
                local_offset += 1
            else:
                break
        if not is_letter(char):
            return True, {'offset': local_offset, 'lexeme': 'DecInt'}
        else:
            return False, {}
    else:
        return False, {}

#
# def is_bin_int(chars):
#     chars = chars.lower()
#
#     # pattern = r'b'
#     # if not re.match(pattern, chars):
#     if not chars.endswith("b"):
#         return False
#
#     chars = chars.replace('b', '')
#     for ch in chars:
#         if ch < "0" or ch > "1":
#             return False
#     return True
#
#
# def is_oct_int(chars):
#     chars = chars.lower()
#     if not chars.endswith("c"):
#         return False
#
#     chars = chars.replace('c', '')
#     for ch in chars:
#         if ch < "0" or ch > "7":
#             return False
#     return True
#
#
# # def is_dec_int(chars):
# #     chars = chars.lower()
# #     if chars.endswith('d'):
# #         chars = chars.replace('d', '')
# #
# #     for ch in chars:
# #         if ch < "0" or ch > "9":
# #             return False
# #     return True
#
#
# def is_hex_int(chars):
#     chars = chars.lower()
#     if chars.endswith('h'):
#         return False
#
#     chars = chars.replace('h', '')
#     for ch in chars:
#         if not ('0' <= ch <= '9' or 'a' <= ch <= 'f'):
#             return False
#     return True
#
#
# # REAL
# def is_real(chars):
#     pattern_one = r'\d*e(\+|\-)?\d+$'
#     pattern_two = r'\d*.\d*(e(\+|\-)?\d+)?$'
#     if re.match(pattern_one, chars):
#         # print('pattern one')
#         return True
#     elif re.match(pattern_two, chars):
#         # print('pattern two')
#         return True
#     else:
#         return False
