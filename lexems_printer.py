__author__ = 'Nikita'

import sys

error_counter = 0


def print_lexeme(output_file, row, lexeme, value, error_message):
    global error_counter

    if lexeme:
        if lexeme == 'Real':
            output_file.write('{}\tlex:{}\treal:{}\tval:{}\n'.format(row, lexeme, value, float(value)))
        elif lexeme == 'Int':
            if value.endswith('b'):
                digit_base = 2
            elif value.endswith('c'):
                digit_base = 8
            elif value.endswith('h'):
                digit_base = 16
            else:
                digit_base = 10
            if digit_base != 10 or (digit_base == 10 and value.endswith('d')):
                value = value[:len(value)-1]

            output_file.write('{}\tlex:{}\tint:{}\tval:{}\n'.format(row, lexeme, value, int(value, digit_base)))
        elif lexeme == 'Error':
            output_file.write('{}\tlex:{}\tval:{}\n'.format(row, lexeme, value))
            print(error_message)
            error_counter += 1
        elif lexeme == 'EOF':
            output_file.write('{}\tlex:{}\tval:{}\n'.format(row, lexeme, value))
            if error_counter == 0:
                print('OK')
        else:
            output_file.write('{}\tlex:{}\tval:{}\n'.format(row, lexeme, value))
    else:
        print('ERROR: empty lexeme or None')
        sys.exit(0)