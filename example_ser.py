# -*- coding: utf-8 -*-
import sys
import os


class MyException(Exception):
    def __init__(self, _type, value):
        Exception.__init__(self)
        self.type = _type
        self.value = value


class Token:
    def __init__(self, identifier='', value='', type_token='', recval=''):
        self.id = identifier
        self.value = value
        self.type = type_token
        self.recval = recval
        self.num_str = 0

class Scanner:
    def __init__(self):
        self.source, self.result = self.open_files()
        self.token = Token()
        self.char = ' '
        self.num_str = 1
        self.errors = 0
        self.SpecialWords = {
            # verbal signs
            'proc': 'Proc', 
            'else': 'Else', 'while': 'While', 
            'do': 'Do', 'of': 'Of', 
            'case': 'Case', 'or': 'Or', 
                        # general special worlds
            'int': 'TypeInt', 'real': 'TypeReal',
            'skip': 'Skip', 'space': "Space", 'tab': 'Tab',
            'goto': 'Goto',
            'read': 'Read', 'write': 'Write',
            'cast': 'Cast',
            'break': 'Break',
        }
        self.SpecialSymbols = {
            
            '*': 'Mul', '/': 'Div', '%': 'Mod',
            '+': 'Add', '-': 'Min', '=': 'Let',
            '==': 'EQ', '!=': 'NE', '<': 'LT',
            '>': 'GT', '<=': 'LE', '>=': 'GE',
            # general special symbols
            '': 'eof',
            '(': 'LRB', ')': 'RRB', '[': 'LSB', ']': 'RSB',
            '{': 'LCB', '}': 'RCB',
            ':': 'Colon', ',': 'Comma',
            ';': 'Semicolon',
            '!': 'Error'
        }
        self.IdentifiersLexemes = {
            'id': 'Id',
            'label': 'Label',
            'error': 'Error',
            'int': 'Int', 'real': 'Real',
            'comment': 'Comment'
        }

        self.CharsAlphabet = ("_", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
                              "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                              "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                              "r", "s", "t", "u", "v", "w", "x", "y", "z")
        
        self.CharsNumSystem = {
            'b': (2,  ['0', '1']),
            'c': (8,  ["0", "1", "2", "3", "4", "5", "6", "7"]),
            'd': (10, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]),
            'h': (16, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                       "A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f"])
        }

    @staticmethod
    def open_files():
        try:
            min_num_params = 3
            if len(sys.argv) < min_num_params:
                print('Error:Params:The number of parameters is less than two')
                sys.exit()
            file_name_cod = sys.argv[1]
            file_name_lexeme = sys.argv[2]

            if not os.path.exists(file_name_cod):
                print('Error:Params:' + file_name_cod + ' File does not exist')
                sys.exit()

            source = open(file_name_cod, 'r')
            result = open(file_name_lexeme, 'w')

            return source, result
        except OSError:
            print('Error:Params:File not available')
            sys.exit()

    def scanner(self):
        tokens = []
        self.get_next_token()
        while self.token.id != self.SpecialSymbols['']:
            if self.token.id != self.IdentifiersLexemes['comment']:
                tokens.append(self.token)
                lexeme_string = self.lexeme_to_string()
                self.result.write(lexeme_string)
            self.get_next_token()
        if self.errors == 0:
            
            return tokens
        else:
            return False

    def lexeme_to_string(self):
        string = str(self.token.num_str) + '\tlex:' + str(self.token.id)
        if self.token.type != '':
            string += '\t' + self.token.type + ':' + self.token.recval
        if self.token.value != '':
            string += '\tval:' + self.token.value
        string += '\n'
        return string

    def get_next_token(self):
        self.token = Token()
        try:
            while self.char.isspace():
                if self.char == '\n':
                    self.num_str += 1
                self.get_next_char()

            self.token.num_str = self.num_str

            if self.char == '':
                self.token.id = self.SpecialSymbols[self.char]
                return True

            
            elif self.char == '/':
                value = self.char
                self.get_next_char()
                if self.char != '*':
                    if value in self.SpecialSymbols.keys():
                        self.token.id = self.SpecialSymbols[value]
                        self.token.value = value
                    else:
                        raise MyException('Lexeme is not defined', value)
                    return True
                self.get_next_char()
                end_comment = False
                while not end_comment:
                    if self.char != '*':
                        if self.char == '\n':
                            self.num_str += 1
                        self.get_next_char()
                    elif self.char == '*':
                        self.get_next_char()
                        if self.char == '/':
                            end_comment = True
                    elif self.char == '':
                        end_comment = True
                self.get_next_char()
                self.token.id = self.IdentifiersLexemes['comment']
                return True

            elif self.char in self.SpecialSymbols.keys():
                self.check_special_symbol()
                return True

            elif self.char.isdigit() or self.char == '.':
                value = self.check_int()
                # label INT

                if self.token.id == '':
                    self.check_real(value)
                    # zero check
                if self.token.id == '':
                    raise MyException("Number is not defined", value)

                return True

            elif self.char in self.CharsAlphabet:
                self.check_special_word_or_id()
                
                return True
            else:
                value = ''
                while not self.char_space_or_special_symbol():
                    value += self.char
                    self.get_next_char()
                except_type = 'Lexeme is not defined'
                raise MyException(except_type, value)

        except MyException as ex:
            self.errors += 1
            while not self.char.isspace() and self.char not in self.SpecialSymbols.keys():
                ex.value += self.char
                self.get_next_char()
            while self.char not in ('\n', ''):
                self.get_next_char()
            self.token.id = self.IdentifiersLexemes['error']
            self.token.value = ex.value
            print('Error:' + str(self.num_str) + ':' + str(ex.value), ex.type)
            return False

    def get_next_char(self):
        self.char = self.source.read(1)

    def char_space_or_special_symbol(self):
        if self.char.isspace() or self.char in self.SpecialSymbols.keys():
            if self.char == '!':
                self.get_next_char()
                if self.char != '=':
                    return False
            return True
        else:
            return False
    
    def check_special_word_or_id(self):
            value = ''
            while self.char in self.CharsAlphabet:
                value += self.char
                self.get_next_char()
            if self.char_space_or_special_symbol():
                if value in self.SpecialWords.keys():
                    self.token.id = self.SpecialWords[value]
                    self.token.value = value
                #elif value == 'rem':
                else:
                    self.token.id = self.IdentifiersLexemes['id']
                    self.token.value = value
                return True

            if self.char.isdigit():
                while self.char in self.CharsAlphabet or self.char.isdigit():
                    value += self.char
                    self.get_next_char()
                if not self.char_space_or_special_symbol():
                    raise MyException("Expected space or special symbol", value)
                self.token.id = self.IdentifiersLexemes['id']
                self.token.value = value
                return True
    
    def check_special_symbol(self):
        value = self.char
        self.get_next_char()

        if self.char == '=' and value in ('=', '!', '<', '>'):
            value += self.char
            self.get_next_char()
        elif value == '!':
            raise MyException("Expected '='", value)

        self.token.id = self.SpecialSymbols[value]
        self.token.value = value
        return True
    
    def check_int(self):
        value = ''
        for char_radix in ('b', 'c', 'd', 'h'):
            radix = self.CharsNumSystem[char_radix][0]
            permissible_number = self.CharsNumSystem[char_radix][1]
            while self.char in permissible_number:
                value += self.char
                self.get_next_char()
            if self.char.lower() == char_radix:
                value += self.char
                self.get_next_char()
                if self.char_space_or_special_symbol():
                    if not self.check_num_str(value[:-1], permissible_number):
                        raise MyException("Invalid character in " + str(radix) + " system number", value)
                    if radix == 16 and value[0].isalpha():
                        raise MyException(str(radix) + " cant begin with letter", value)

                    self.token.id = self.IdentifiersLexemes['int']
                    self.token.value = value
                    self.token.type = self.IdentifiersLexemes['int'].lower()
                    self.token.recval = str(int(value[:-1], radix))
                    if not int(self.token.recval) <= 2147483647:
                        raise MyException('The number out of range', self.token.recval)
                    return True
            elif radix == 10 and self.char_space_or_special_symbol() and self.check_num_str(value, permissible_number):
                self.token.id = self.IdentifiersLexemes['int']
                self.token.value = value
                self.token.type = self.IdentifiersLexemes['int'].lower()
                self.token.recval = str(int(value, radix))
                if not int(self.token.recval) <= 2147483647:
                    raise MyException('The number out of range', self.token.recval)
                return True
        return value
    
    def check_real(self, value):
        if not self.num_mb_real(value):
            return False
        if self.only_number_in_str(value):
            num_str = ''
            if self.char == '.':
                num_str += self.char
                self.get_next_char()
                while self.char.isdigit():
                    num_str += self.char
                    self.get_next_char()

                if value == '' and len(num_str) == 1:
                    raise MyException('Expected num str', '.')

                if self.char in ('e', 'E'):
                    num_str += self.char
                    self.get_next_char()
                    if self.char in ('+', '-'):
                        num_str += self.char
                        self.get_next_char()
                    if not self.char.isdigit():
                        raise MyException("Expected number", value + '.' + num_str)
                    while self.char.isdigit():
                        num_str += self.char
                        self.get_next_char()

            elif self.char in ('e', 'E'):
                num_str += self.char
                self.get_next_char()
                if self.char in ('+', '-'):
                    num_str += self.char
                    self.get_next_char()
                if not self.char.isdigit():
                    raise MyException("Expected number", value + '.' + num_str)
                while self.char.isdigit():
                    num_str += self.char
                    self.get_next_char()
            value += num_str

        elif 'e' in value.lower():
            if self.char in ('+', '-'):
                value += self.char
                self.get_next_char()
                if not self.char.isdigit():
                    raise MyException("Expected number", value)
                while self.char.isdigit():
                    value += self.char
                    self.get_next_char()
        else:
            if self.char not in ('e', 'E'):
                raise MyException("Expected 'E'", value)
            value += self.char
            self.get_next_char()
            if self.char in ('+', '-'):
                value += self.char
                self.get_next_char()
            if not self.char.isdigit():
                raise MyException("Expected number", value)
            while self.char.isdigit():
                value += self.char
                self.get_next_char()

        if not self.char_space_or_special_symbol():
                raise MyException("Expected space/special symbol", value)

        self.token.id = self.IdentifiersLexemes['real']
        self.token.value = value
        self.token.type = self.IdentifiersLexemes['real'].lower()
        self.token.recval = self.real_to_exponential(value)
        if not (float(self.token.recval) <= 3.402823466e+38) or self.token.recval == float('inf'):
            raise MyException('The number out of range', self.token.value)
        return True
    
    def check_label(self):
        if self.token.id == self.IdentifiersLexemes['id']:
            while self.char.isspace():
                if self.char == '\n':
                    self.num_str += 1
                self.get_next_char()

            if self.char == ':':
                self.token.id = self.IdentifiersLexemes['label']
                self.token.value = self.token.value
                self.token.type = ''
                self.token.recval = ''
                self.get_next_char()
            return True

    @staticmethod
    def num_mb_real(num):
        exponent = False
        for i in num:
            if i in ('e', 'E'):
                if not exponent:
                    exponent = True
                else:
                    return False
            elif not i.isdigit():
                return False

        return True

    @staticmethod
    def real_to_exponential(num):
        if float(num) in (0, float('inf')):
            return num
        num = str(float(num))
        std_num = num
        pos = num.lower().find('e')
        degree = 0
        if pos != -1:
            degree = int(num[pos+1:])
            num = num[:pos]

        pos = num.find('.')
        if pos == -1:
            integer = num
            fraction = '0'
        else:
            integer = num[:pos]
            fraction = num[pos + 1:]
        if integer[0] == '0':
            pos = 0
            while fraction[pos] == '0':
                degree -= 1
                fraction = fraction[1:]

            degree -= 1
            integer = fraction[0]
            fraction = fraction[1:]
            num = integer + '.' + fraction + 'e' + str(degree)
        else:
            if len(integer) == 1:
                return std_num
            degree += pos - 1
            fraction = integer[1:pos] + fraction
            integer = integer[0]
            while fraction[-1] == '0' and len(fraction) > 1:
                fraction = fraction[:-1]
            num = integer + '.' + fraction + 'e' + str(degree)

        return num

    @staticmethod
    def check_num_str(num_str, chars_num):
        if num_str == '':
            return False

        for num in num_str:
            equal = False
            for char in chars_num:
                if char == num:
                    equal = True
                    break
            if not equal:
                return False
        return True

    @staticmethod
    def only_number_in_str(string):
        for i in string:
            if not i.isdigit():
                return False
        return True


class Tree:
    def __init__(self, tag=None, value=None, num_str=0):
        self.num_str = num_str
        self.tag = tag
        self.value = value
        self.nodes = []
        self.atributes = []


class Parser:
    def __init__(self):
        min_arguments = 4
        if len(sys.argv) < min_arguments:
            print('Error:Params: The number of parameters less 3')
            sys.exit(1)

        file_name_tree = sys.argv[3]

        self.scanner = Scanner()
        self.lexemes = self.scanner.scanner()
        if self.lexemes is False:
            exit(1)
        self.num_lexeme = 0

        try:
            self.tree = open(file_name_tree, 'w')
        except OSError:
            print('Error:Params:File not available')
            sys.exit()

        self.token = Token()

        self.labels = []

        self.in_cycle = False
        self.in_operand = False

        self.SignsSurgery = [
            'Add', 'Min', 'Mul', 'Div', 'Mod',
            'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'
        ]
        self.QualifierWords = {'skip': 'Skip', 'space': "Space", 'tab': 'Tab'}
        self.SpecialWords = self.scanner.SpecialWords
        self.SpecialSymbols = self.scanner.SpecialSymbols
        self.IdentifiersLexemes = {
            'id': 'Id',
            'label': 'Label',
            'break': 'Break',
            'of': 'Of, Or',
            'do': 'Do',
            'error': 'Error',
            'eof': 'EOF',
            'int': 'Int', 'real': 'Real'
        }
        self.IDWordsAndSymbolAfterOperator = [
            'Semicolon', 'Else', 'Or'
        ]

    def get_next_lexeme(self):
        if self.num_lexeme == -1:
            self.token.id = self.SpecialSymbols['']
        else:
            self.token = self.lexemes[self.num_lexeme]
            self.num_lexeme += 1
            if self.num_lexeme > len(self.lexemes) - 1:
                self.num_lexeme = -1

    def parsing(self):
        try:
            tree = self.is_program()
            self.tree.write('<?xml version="1.0" ?>\n')
            self.output_tree(tree, 0)
            print('OK')
            return tree
        except MyException as ex:
            msg_str = "Error:" + str(ex.type) + ':'
            if self.token.value != '':
                msg_str += '"' + self.token.value + '"'
            msg_str += ex.value
            print(msg_str)
            return False

    def output_tree(self, tree, n):
        self.tree.write('\t'*n + '<' + tree.tag)
        # if tree.num_str != 0:
        #    self.tree.write(str(tree.num_str))
        if tree.value is not None:
            self.tree.write('="'+tree.value+'"')
        for atr in tree.atributes:
            self.tree.write(' ' + atr.tag + '="' + atr.value + '"')
        if len(tree.nodes) == 0:
            self.tree.write('/>\n')
        else:
            self.tree.write('>\n')
            for i in tree.nodes:
                self.output_tree(i, n+1)
            self.tree.write('\t'*n + '</' + tree.tag + '>' + '\n')

    #################################################################
    
    def is_program(self):
        if len(self.lexemes) == 0:
            raise MyException(self.tree.name, 'File empty')

        tree = Tree(tag='program')
        self.get_next_lexeme()
        node = None
        while self.token.id != self.SpecialSymbols['']:
            program_funcs = [self.is_description, self.is_operator, self.is_proc]
            for func in program_funcs:
                node = func()
                if node:
                    break
            if not node:
                raise MyException(self.token.num_str, 'Expected description|operator|procedure')
            tree.nodes.append(node)
            if self.token.id != self.SpecialSymbols[';']:
                raise MyException(self.token.num_str, 'Expected ";"')
            self.get_next_lexeme()

        return tree
    
    def is_compound(self):
        if self.token.id != self.SpecialSymbols['{']:
            return False
        start_line = self.token.num_str
        compound_tree = Tree(tag='compound', num_str=self.token.num_str)
        self.get_next_lexeme()

        op_node = self.is_operator()
        if not op_node:
            raise MyException(self.token.num_str, 'Expected operator')
        while op_node:
            compound_tree.nodes.append(op_node)

            if self.token.id != self.SpecialSymbols[';']:
                raise MyException(self.token.num_str, 'Expected ";"')
            self.get_next_lexeme()

            op_node = self.is_operator()

        if self.token.id != self.SpecialSymbols['}']:
            raise MyException(start_line, 'Expected "}"')
        self.get_next_lexeme()
        return compound_tree
    
    def is_description(self):
        if self.token.id not in (self.SpecialWords['int'], self.SpecialWords['real']):
            return False
        dfn_node = Tree(tag='dfn', num_str=self.token.num_str)
        dfn_node.atributes.append(Tree(tag='type', value=self.token.id.lower(), num_str=self.token.num_str))
        brief_nodes = []

        expected_identifier = True
        while expected_identifier:
            self.get_next_lexeme()
            if self.token.id != self.IdentifiersLexemes['id']:
                raise MyException(self.token.num_str, 'Expected Identifier')

            brief_node = Tree(tag='brief', num_str=self.token.num_str)
            brief_node.atributes.append(Tree(tag='name', value=self.token.value, num_str=self.token.num_str))

            self.get_next_lexeme()
            if self.token.id == self.SpecialSymbols['[']:
                self.get_next_lexeme()
                if self.token.id != self.IdentifiersLexemes['int']:
                    raise MyException(self.token.num_str, 'Expected integer')
                if str(self.token.recval) == '0':
                    raise MyException(self.token.num_str, 'Invalid array size')
                brief_node.atributes.append(Tree(tag='length', value=self.token.value, num_str=self.token.num_str))
                self.get_next_lexeme()
                if self.token.id != self.SpecialSymbols[']']:
                    raise MyException(self.token.num_str, 'Expected "]"')
                self.get_next_lexeme()
            brief_nodes.append(brief_node)
            if self.token.id != self.SpecialSymbols[',']:
                expected_identifier = False
                if len(brief_nodes) > 1:
                    for i in brief_nodes:
                        dfn_node.nodes.append(i)
                elif len(brief_nodes) == 1:
                    for i in brief_node.atributes:
                        dfn_node.atributes.append(i)
        return dfn_node

    def get_previous_lexeme(self, num_lexeme=-1):
        if num_lexeme == -1:
            self.num_lexeme -= len(self.lexemes) - 1
        else:
            self.num_lexeme = num_lexeme - 1
        self.get_next_lexeme()

    def is_operator(self):
        label_node = None
        if self.token.id == self.IdentifiersLexemes['id']:
            checkpoint = self.num_lexeme
            label_name = self.token.value
            label_num_str = self.token.num_str
            self.get_next_lexeme()
            if self.token.id == self.SpecialSymbols[':']:
                if label_name in self.labels:
                    raise MyException(label_num_str, 'Repeated label name')
                self.labels.append(label_name)
                label_node = Tree(tag='label', num_str=label_num_str)
                label_node.atributes.append(Tree(tag='name', value=label_name, num_str=label_num_str))
                self.get_next_lexeme()
            else:
                self.get_previous_lexeme(checkpoint)
        unlabelled_node = self.is_unlabelled()

        if not unlabelled_node:
            if label_node is not None:
                raise MyException(self.token.num_str, 'Expected unlabelled')
            return False

        operator_node = Tree(tag='clause', num_str=self.token.num_str)
        if label_node is not None:
            operator_node.nodes.append(label_node)
        operator_node.nodes.append(unlabelled_node)

        return operator_node

    def is_unlabelled(self):
        unlabelled_functions = [self.is_compound, self.is_assignment, self.is_adduction,
                                self.is_transition, self.is_conditional, self.is_cycle,
                                self.is_input, self.is_output, self.is_call, self.is_empty
                                ]
        if self.in_cycle and self.token.id == self.SpecialWords['break']:
            self.get_next_lexeme()
            return Tree(tag='break', num_str=self.token.num_str)
        for func in unlabelled_functions:
            unlabelled_node = func()
            if unlabelled_node:
                return unlabelled_node

        return False

    def is_empty(self):
        if self.token.id in self.IDWordsAndSymbolAfterOperator:
            return Tree(tag='empty', num_str=self.token.num_str)
        return False

    def is_transition(self):
        if self.token.id != self.SpecialWords['goto']:
            return False
        goto_node = Tree(tag='goto', num_str=self.token.num_str)
        self.get_next_lexeme()

        if self.token.id != self.IdentifiersLexemes['id']:
            raise MyException(self.token.num_str, 'Expected label')
        goto_node.atributes.append(Tree(tag='label', value=self.token.value, num_str=self.token.num_str))
        self.get_next_lexeme()

        return goto_node

    def is_input(self):
        if self.token.id != self.SpecialWords['read']:
            return False
        read_node = Tree(tag='read', num_str=self.token.num_str)
        expected_variable = True
        while expected_variable:
            self.get_next_lexeme()
            variable_node = self.is_variable()
            if not variable_node:
                raise MyException(self.token.num_str, 'Expected variable')  # ���������� ��������� ����������
            read_node.nodes.append(variable_node)

            if self.token.id != self.SpecialSymbols[',']:
                expected_variable = False
        return read_node

    def is_output(self):
        if self.token.id != self.SpecialWords['write']:
            return False
        write_node = Tree(tag='write', num_str=self.token.num_str)
        expected_argument = True
        while expected_argument:
            self.get_next_lexeme()
            argument_node = self.is_qualifier()
            if argument_node:
                self.get_next_lexeme()
            else:
                argument_node = self.is_expression()
                if not argument_node:
                    raise MyException(self.token.num_str, 'Expected qualifier|expression')
            write_node.nodes.append(argument_node)
            if self.token.id != self.SpecialSymbols[',']:
                expected_argument = False
        return write_node

    def is_variable(self):
        if self.token.id != self.IdentifiersLexemes['id']:
            return False
        variable_node = Tree(tag='var', num_str=self.token.num_str)
        variable_node.atributes.append(Tree(tag='name', value=self.token.value, num_str=self.token.num_str))
        self.get_next_lexeme()
        if self.token.id == self.SpecialSymbols['[']:
            self.get_next_lexeme()
            index_node = self.is_index()
            if not index_node:
                raise MyException(self.token.num_str, 'Expected index')
            variable_node.atributes.append(index_node)
            self.get_next_lexeme()
            if self.token.id != self.SpecialSymbols[']']:
                raise MyException(self.token.num_str, 'Expected "]"')
            self.get_next_lexeme()
        return variable_node

    def is_index(self):
        if self.token.id in (self.IdentifiersLexemes['id'],
                             self.IdentifiersLexemes['int']):
            return Tree(tag='index', value=self.token.value, num_str=self.token.num_str)
        return False

    def is_qualifier(self):
        if self.token.id in self.QualifierWords.values():
            qualifier_node = Tree(tag='qualifier', num_str=self.token.num_str)
            qualifier_node.atributes.append(Tree(tag='kind', value=self.token.value, num_str=self.token.num_str))
            return qualifier_node
        return False

    #################################################################
    
    def is_assignment(self):
        checkpoint = self.num_lexeme
        variable_node = self.is_variable()
        if not variable_node:
            return False
        if self.token.id != 'Let':
            self.get_previous_lexeme(checkpoint)
            return False

        assign_node = Tree(tag='assign', num_str=self.token.num_str)
        assign_node.nodes.append(variable_node)
        self.get_next_lexeme()

        expression_node = self.is_expression()
        if not expression_node:
            raise MyException(self.token.num_str, 'Expected expression')
        assign_node.nodes.append(expression_node)
        return assign_node
    
    def is_expression(self):
        first_summand_node = self.is_summand()
        if not first_summand_node:
            return False
        op_nodes = []
        expression_words = ('EQ', 'NE', 'LT', 'GT', 'LE', 'GE')
        while self.token.id in expression_words:
            op_node = Tree(tag='op', num_str=self.token.num_str)
            kind = self.token.id.lower()
            kind_node = Tree(tag='kind', value=kind, num_str=self.token.num_str)
            self.get_next_lexeme()

            summand_node = self.is_summand()
            if not summand_node:
                raise MyException(self.token.num_str, 'Expected summand')

            op_node.atributes.append(kind_node)
            op_node.nodes.append(summand_node)
            op_nodes.append(op_node)

        if len(op_nodes) == 0:
            return first_summand_node

        op_nodes.reverse()
        op_nodes.append(first_summand_node)
        op_tree = self.create_op_tree(op_nodes)

        return op_tree

    def is_summand(self):
        first_multiplier_node = self.is_multiplier()
        if not first_multiplier_node:
            return False

        op_nodes = []
        summand_words = ('Add', 'Min')
        while self.token.id in summand_words:
            op_node = Tree(tag='op', num_str=self.token.num_str)
            kind = self.token.id.lower()
            kind_node = Tree(tag='kind', value=kind, num_str=self.token.num_str)
            self.get_next_lexeme()

            multiplier_node = self.is_multiplier()
            if not multiplier_node:
                raise MyException(self.token.num_str, 'Expected multiplier')

            op_node.atributes.append(kind_node)
            op_node.nodes.append(multiplier_node)
            op_nodes.append(op_node)

        if len(op_nodes) == 0:
            return first_multiplier_node

        op_nodes.reverse()
        op_nodes.append(first_multiplier_node)
        op_tree = self.create_op_tree(op_nodes)

        return op_tree

    def is_multiplier(self):
        first_unary_node = self.is_unary()
        if not first_unary_node:
            return False

        last_tag = first_unary_node.tag
        op_nodes = []
        mult_words = ('Mul', 'Div', 'Mod')
        while self.token.id in mult_words:
            op_node = Tree(tag='op', num_str=self.token.num_str)
            kind = self.token.id.lower()
            kind_node = Tree(tag='kind', value=kind, num_str=self.token.num_str)
            self.get_next_lexeme()

            unary_node = self.is_unary()
            if kind == 'mod' and (unary_node.tag == 'real' or last_tag == 'real'):
                raise MyException(self.token.num_str, 'Integer is not valid for mod operation')
            if not unary_node:
                raise MyException(self.token.num_str, 'Expected unary')
            last_tag = unary_node.tag

            op_node.atributes.append(kind_node)
            op_node.nodes.append(unary_node)
            op_nodes.append(op_node)

        if len(op_nodes) == 0:
            return first_unary_node

        op_nodes.reverse()
        op_nodes.append(first_unary_node)
        op_tree = self.create_op_tree(op_nodes)

        return op_tree

    def is_unary(self):
        kind_node = None
        if self.token.id == 'Min':
            kind_node = Tree(tag='kind', value=self.token.id, num_str=self.token.num_str)
            self.get_next_lexeme()
        therm_node = self.is_therm()
        if therm_node:
            if kind_node is not None:
                op_node = Tree(tag='op', num_str=self.token.num_str)
                op_node.nodes.append(kind_node)
                op_node.nodes.append(therm_node)
                therm_node = op_node
            return therm_node
        else:
            if kind_node is not None:
                raise MyException(self.token.num_str, 'Expected therm')
        return False

    def is_therm(self):
        therm_functions = [self.is_number, self.is_variable]
        for func in therm_functions:
            therm_node = func()
            if therm_node:
                return therm_node

        if self.token.id == self.SpecialSymbols['(']:
            self.get_next_lexeme()
            therm_node = self.is_expression()
            if not therm_node:
                raise MyException(self.token.num_str, 'Expected expression')
            if not self.token.id == self.SpecialSymbols[')']:
                raise MyException(self.token.num_str, 'Expected ")"')
            self.get_next_lexeme()
            return therm_node

        return False
    
    def is_adduction(self):
        checkpoint = self.num_lexeme
        variable_node = self.is_variable()
        if not variable_node:
            return False

        if self.token.id != 'Cast':
            self.get_previous_lexeme(checkpoint)
            return False
        self.get_next_lexeme()
        variables = list()
        variables.append(variable_node)

        variable_node = self.is_variable()
        if not variable_node:
            raise MyException(self.token.num_str, 'Expected variable')
        variables.append(variable_node)

        cast_node = Tree(tag='cast', num_str=self.token.num_str)
        for var in variables:
            cast_node.nodes.append(var)
        return cast_node

    def is_number(self):
        if self.token.id in (self.IdentifiersLexemes['int'], self.IdentifiersLexemes['real']):
            number_node = Tree(tag=self.token.type, num_str=self.token.num_str)
            number_node.atributes.append(Tree(tag='val', value=self.token.recval, num_str=self.token.num_str))
            self.get_next_lexeme()
            return number_node
        return False

    def create_op_tree(self, op_nodes):
        if len(op_nodes) == 1:
            return op_nodes[0]
        op_nodes[0].nodes.append(self.create_op_tree(op_nodes[1:]))
        return op_nodes[0]

    #################################################################
    
    def is_conditional(self):
        if self.token.id != self.SpecialWords['case']:
            return False
        start_line = self.token.num_str
        self.get_next_lexeme()
        conditional_tree = Tree(tag='switch', num_str=self.token.num_str)

        expression_node = self.is_expression()
        if not expression_node:
            raise MyException(self.token.num_str, 'Expected expression')
        conditional_tree.nodes.append(expression_node)

        if self.token.id != self.SpecialWords['of']:
            raise MyException(self.token.num_str, 'Expected "then"')
        of_node = Tree(tag='of', num_str=self.token.num_str)
        self.get_next_lexeme()

        lbls = list()
        if self.token.id != self.IdentifiersLexemes['int']:
            raise MyException(self.token.num_str, 'Expected int')
        number_node = Tree(tag=self.token.type, num_str=self.token.num_str)
        number_node.atributes.append(Tree(tag='val', value=self.token.recval, num_str=self.token.num_str))
        of_node.nodes.append(number_node)
        lbls.append(self.token.recval)
        self.get_next_lexeme()

        if self.token.id != self.SpecialSymbols[':']:
            raise MyException(self.token.num_str, 'Expected ":"')
        self.get_next_lexeme()

        unlabelled_node = self.is_unlabelled()
        if not unlabelled_node:
            raise MyException(self.token.num_str, 'Expected operator')
        of_node.nodes.append(unlabelled_node)
        conditional_tree.nodes.append(of_node)


        while self.token.id == self.SpecialWords['or']:
            or_node = Tree(tag='or', num_str=self.token.num_str)
            self.get_next_lexeme()

            if self.token.id != self.IdentifiersLexemes['int']:
                raise MyException(self.token.num_str, 'Expected int')
            if self.token.recval in lbls:
                raise MyException(self.token.num_str, 'Repeated label name')
            number_node = Tree(tag=self.token.type, num_str=self.token.num_str)
            number_node.atributes.append(Tree(tag='val', value=self.token.recval, num_str=self.token.num_str))
            or_node.nodes.append(number_node)
            self.get_next_lexeme()

            if self.token.id != self.SpecialSymbols[':']:
                raise MyException(self.token.num_str, 'Expected ":"')
            self.get_next_lexeme()

            unlabelled_node = self.is_unlabelled()
            if not unlabelled_node:
                raise MyException(self.token.num_str, 'Expected operator')
            or_node.nodes.append(unlabelled_node)
            conditional_tree.nodes.append(of_node)

        if self.token.id == self.SpecialWords['else']:
            else_node = Tree(tag='case', num_str=self.token.num_str)
            self.get_next_lexeme()

            unlabelled_node = self.is_unlabelled()
            if not unlabelled_node:
                raise MyException(self.token.num_str, 'Expected operator')
            else_node.nodes.append(unlabelled_node)
            conditional_tree.nodes.append(else_node)

        return conditional_tree
    #################################################################
    
    def is_cycle(self):
        if self.token.id != self.SpecialWords['while']:
            return False
        start_line = self.token.num_str
        cycle_tree = Tree(tag='while', num_str=self.token.num_str)
        self.get_next_lexeme()

        if not self.in_cycle:
            change_in_cycle = True
            self.in_cycle = True
        else:
            change_in_cycle = False

        expression_node = self.is_expression()
        if not expression_node:
            raise MyException(self.token.num_str, 'Expected expression')
        cycle_tree.nodes.append(expression_node)

        if self.token.id != self.SpecialWords['do']:
            raise MyException(self.token.num_str, 'Expected "do"')
        self.get_next_lexeme()

        unlabelled_node = self.is_unlabelled()
        if not unlabelled_node:
            raise MyException(self.token.num_str, 'Expected unlabelled')
        cycle_tree.nodes.append(unlabelled_node)

        if change_in_cycle:
            self.in_cycle = False

        return cycle_tree
    #################################################################
    
    def is_proc(self):
        if self.token.id != self.SpecialWords['proc']:
            return False
        self.get_next_lexeme()
        if self.token.id != self.IdentifiersLexemes['id']:
            raise MyException(self.token.num_str, 'Expected id')

        proc_tree = Tree(tag='proc', num_str=self.token.num_str)
        id_node = Tree(tag='var', num_str=self.token.num_str)
        id_node.atributes.append(Tree(tag='name', value=self.token.value, num_str=self.token.num_str))
        proc_tree.nodes.append(id_node)
        self.get_next_lexeme()

        description_node = self.is_description()
        while description_node:
            proc_tree.nodes.append(description_node)
            if self.token.id != self.SpecialSymbols[';']:
                raise MyException(self.token.num_str, 'Expected ";"')
            self.get_next_lexeme()
            description_node = self.is_description()

        component_node = self.is_compound()
        if not component_node:
            raise MyException(self.token.num_str, 'Expected component')
        proc_tree.nodes.append(component_node)

        return proc_tree
    #################################################################
    
    def is_call(self):
        if self.token.id != self.IdentifiersLexemes['id']:
            return False
        call_tree = Tree(tag='call', num_str=self.token.num_str)
        id_node = Tree(tag='var', num_str=self.token.num_str)
        id_node.atributes.append(Tree(tag='name', value=self.token.value, num_str=self.token.num_str))
        call_tree.nodes.append(id_node)
        self.get_next_lexeme()
        if self.token.id != self.SpecialSymbols['(']:
            raise MyException(self.token.num_str, ' Expected "("')
        self.get_next_lexeme()

        variable_node = self.is_variable()
        while variable_node:
            call_tree.nodes.append(variable_node)
            if self.token.id != self.SpecialSymbols[',']:
                break
            self.get_next_lexeme()
            variable_node = self.is_variable()
            if not variable_node:
                raise MyException(self.token.num_str, ' Expected variable')

        if self.token.id != self.SpecialSymbols[')']:
            raise MyException(self.token.num_str, 'Expected ")"')
        self.get_next_lexeme()

        return call_tree


if __name__ == '__main__':
    parser = Parser()
    parser.parsing()
