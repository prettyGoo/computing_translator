__author__ = 'Nikita'

import sys

error_counter = 0


def print_lexeme(output_file, row, lexeme, value, error_message):
    global error_counter

    if lexeme:
        if lexeme == 'Real':
            max_float = 1.701411733e+38
            if float(value) <= max_float:
                output_file.write('{}\tlex:{}\treal:{}\tval:{}\n'.format(row, lexeme, value, float(value)))
            else:
                output_file.write('{}\tlex:{}\tval:{}\n'.format(row, 'Error', value))
                print('Error:{}:{}'.format(row, 'Max float overflow'))
                error_counter += 1
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

            output_file.write('{}\tlex:{}\tint:{}\tval:{}\n'.format(row, lexeme, int(value, digit_base), value))
        elif lexeme == 'Error':
            output_file.write('{}\tlex:{}\tval:{}\n'.format(row, lexeme, value))
            print('Error:{}:{}'.format(row, error_message))
            error_counter += 1
        elif lexeme == 'EOF':
            #output_file.write('{}\tlex:{}\tval:{}\n'.format(row, lexeme, value))
            if error_counter == 0:
                print('OK')
        elif lexeme == 'Space' or lexeme == 'Tab' or lexeme == 'NewLine':
            return
        else:
            output_file.write('{}\tlex:{}\tval:{}\n'.format(row, lexeme, value))
    else:
        print('ERROR: empty lexeme or None')
        sys.exit(0)