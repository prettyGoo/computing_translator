import sys
import os

import indirect


class MyException(Exception):
    def __init__(self, _type, value):
        Exception.__init__(self)
        self.type = _type
        self.value = value


class Token:
    def __init__(self, lexeme='', value='', type_token='', recval='', row=0):
        self.lexeme = lexeme
        self.value = value
        self.type = type_token
        self.recval = recval
        self.row = row


class Tree:
    def __init__(self, tag=None, value=None, num_str=0):
        self.num_str = num_str
        self.tag = tag
        self.value = value
        self.nodes = []
        self.attributes = []


class Parser:
    def __init__(self):
        min_arguments = 4
        if len(sys.argv) < min_arguments:
            print('Error:Params: The number of args is less than 3')
            sys.exit(0)

        output_file = sys.argv[2]
        tree_file = sys.argv[3]

        self.scanner = indirect
        self.scanner.run()

        try:
            file = open(output_file, 'r')
        except FileNotFoundError:
            print('Error:Params: The file you are looking for does not exist\n')
            sys.exit(0)

        file_content = file.read()

        self.lexemes = []
        self.lexemes = self.tokenize_lexemes(file_content)
        if len(self.lexemes) == 0 or (len(self.lexemes) == 1 and self.lexemes[0].lexeme == 'eof'):
            print('Error:Params: Empty file\n')
            exit(0)

        self.num_lexeme = 0

        try:
            self.tree = open(tree_file, 'w')
        except OSError:
            print('Error:Params:Cannot write to given file')
            sys.exit()

        self.token = Token()

        self.labels = []

        self.in_cycle = False
        self.in_operand = False

        self.MathOperations = ['Add', 'Min', 'Mul', 'Div', 'Mod', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE']
        self.IDWordsAndSymbolAfterOperator = ['Semicolon', 'Else', 'Or']

        self.QualifierWords = {'\n': 'Skip', ' ': "Space", '\t': 'Tab'}

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

        self.SpecialWords = {

            '=': 'EQ', '<>': 'NE', '<': 'LT', '>': 'GT', '<=': 'LE', '>=': 'GE',
            '+': 'Add', '-': 'Min', '*': 'Mul', 'div': 'Div', 'mod': 'Mod', ':=': 'Let',
            'var': 'Var',
            'tools': 'Tools',
            'proc': 'Proc',
            'case': 'Case', 'else': 'Else', 'then': 'Then', 'of': 'Of', 'or': 'Or',
            'begin': 'Beg', 'end': 'End',
            'loop': 'Loop',
            'int': 'TypeInt', 'real': 'TypeReal',
            '\n': 'Skip', ' ': "Space", '\t': 'Tab',
            'goto': 'Goto',
            'read': 'Read', 'write': 'Write',
            'cast': 'Cast',
            'break': 'Break',
            'call': 'Call'
        }

        self.SpecialSymbols = {
            '': 'eof',
            '(': 'LRB', ')': 'RRB', '[': 'LSB', ']': 'RSB', '{': 'LCB', '}': 'RCB',
            ':': 'Colon', ';': 'Semicolon', ',': 'Comma',
            '!': 'Error'
        }

    @staticmethod
    def tokenize_lexemes(untokenized_lexemes):
        tokenized_lexemes = []

        for lexeme in untokenized_lexemes.split('\n'):
            lexeme = lexeme.split('\t')
            token = None

            if len(lexeme) == 3:
                row = lexeme[0]
                lex = lexeme[1][4:]
                val = lexeme[2][4:]
                token = Token(row=row, lexeme=lex, value=val)
            elif len(lexeme) == 4:
                row = lexeme[0]
                lex = lexeme[1][4:]
                type = lexeme[2].split(':')[0]
                recval = lexeme[2].split(':')[1]
                val = lexeme[3][4:]
                token = Token(row=row, lexeme=lex, type_token=type, recval=recval, value=val)
            elif lexeme == ['']:
                continue

            if not (token or lexeme):
                sys.exit(1)
            tokenized_lexemes.append(token)

        return tokenized_lexemes

    def parsing(self):
        try:
            tree = self.is_program()
            self.tree.write('<?xml version="1.0" ?>\n')
            self.output_tree(tree, 0)
            print('OK')
            # return tree
        except MyException as ex:
            msg_str = "Error:" + str(ex.type) + ':'
            if self.token.value != '':
                msg_str += '"' + self.token.value + '"'
            msg_str += ex.value
            print(msg_str)
            # return False

    def is_program(self):
        if len(self.lexemes) == 0:
            raise MyException(self.tree.name, 'File empty')

        tree = Tree(tag='program')
        self.get_next_lexeme()

        if self.token.lexeme == self.SpecialWords['var']:
            var_node = Tree(tag='var_declar', num_str=self.token.row)
            expected_description = True
            while expected_description:
                self.get_next_lexeme()
                description_node = self.is_description()
                if not description_node:
                    raise MyException(self.token.row, 'Expected description')
                var_node.nodes.append(description_node)
                if self.token.lexeme != self.SpecialSymbols[';']:
                    expected_description = False
            tree.nodes.append(var_node)

        if self.token.lexeme == self.SpecialWords['tools']:
            tools_node = Tree(tag='tools', num_str=self.token.row)
            expected_proc = True
            while expected_proc:
                self.get_next_lexeme()
                proc_node = self.is_proc()
                if not proc_node:
                    raise MyException(self.token.row, 'Expected procedure')
                tools_node.nodes.append(proc_node)
                if self.token.lexeme != self.SpecialSymbols[';']:
                    expected_proc = False
            tree.nodes.append(tools_node)

        compound_node = self.is_compound()
        if not compound_node:
            raise MyException(self.token.row, 'Expected compound')
        tree.nodes.append(compound_node)

        return tree

    def get_next_lexeme(self):
        if self.num_lexeme == -1:
            self.token.id = self.SpecialSymbols['']
        else:
            self.token = self.lexemes[self.num_lexeme]
            self.num_lexeme += 1
            if self.num_lexeme > len(self.lexemes) - 1:
                self.num_lexeme = -1

    # === END CORE STRUCTURE METHODS ===
    
    def is_compound(self):
        if self.token.lexeme != 'Beg':
            return False
        start_line = self.token.row
        compound_tree = Tree(tag='compound', num_str=self.token.row)

        expected_operator = True
        while expected_operator:
            self.get_next_lexeme()
            if self.token.lexeme == 'End':
                self.get_next_lexeme()
                return compound_tree
            op_node = self.is_operator()
            if not op_node:
                if self.token.lexeme == 'Real':
                    raise MyException(self.token.row, 'Expected correct label')
                else:
                    raise MyException(self.token.row, 'Expected operator')
            compound_tree.nodes.append(op_node)
            if self.token.lexeme != self.SpecialSymbols[';']:
                expected_operator = False

        if self.token.lexeme != 'End':
            raise MyException(start_line, 'Expected "stop"')
        self.get_next_lexeme()
        return compound_tree
    
    def is_description(self):
        if self.token.lexeme not in (self.SpecialWords['int'], self.SpecialWords['real']):
            return False
        dfn_node = Tree(tag='dfn', num_str=self.token.row)
        dfn_node.attributes.append(Tree(tag='type', value=self.token.lexeme.lower(), num_str=self.token.row))
        brief_nodes = []

        expected_identifier = True
        while expected_identifier:
            self.get_next_lexeme()
            if self.token.lexeme != self.IdentifiersLexemes['id']:
                raise MyException(self.token.row, 'Expected Identifier')

            brief_node = Tree(tag='brief', num_str=self.token.row)
            brief_node.attributes.append(Tree(tag='name', value=self.token.value, num_str=self.token.row))

            self.get_next_lexeme()
            if self.token.lexeme == self.SpecialSymbols['[']:
                self.get_next_lexeme()
                if self.token.lexeme != self.IdentifiersLexemes['int']:
                    raise MyException(self.token.row, 'Expected integer')
                if str(self.token.recval) == '0':
                    raise MyException(self.token.row, 'Invalid array size')
                brief_node.attributes.append(Tree(tag='length', value=self.token.value, num_str=self.token.row))
                self.get_next_lexeme()
                if self.token.lexeme != self.SpecialSymbols[']']:
                    raise MyException(self.token.row, 'Expected "]"')
                self.get_next_lexeme()
            brief_nodes.append(brief_node)
            if self.token.lexeme != self.SpecialSymbols[',']:
                expected_identifier = False
                if len(brief_nodes) > 1:
                    for i in brief_nodes:
                        dfn_node.nodes.append(i)
                elif len(brief_nodes) == 1:
                    for i in brief_node.attributes:
                        dfn_node.attributes.append(i)
        return dfn_node

    def get_previous_lexeme(self, num_lexeme=-1):
        if num_lexeme == -1:
            self.num_lexeme -= len(self.lexemes) - 1
        else:
            self.num_lexeme = num_lexeme - 1
        self.get_next_lexeme()

    def is_operator(self):
        label_node = None
        if self.token.lexeme == 'Label':
            label_name = self.token.value[:-1]
            label_num_str = self.token.row
            if label_name in self.labels:
                raise MyException(self.token.row, 'Repeated label name')
            self.labels.append(label_name)
            label_node = Tree(tag='label', num_str=label_num_str)
            label_node.attributes.append(Tree(tag='name', value=label_name, num_str=label_num_str))
            self.get_next_lexeme()

        unlabelled_node = self.is_unlabelled()

        if not unlabelled_node:
            if label_node is not None:
                raise MyException(self.token.row, 'Expected unlabelled')
            return False

        operator_node = Tree(tag='clause', num_str=self.token.row)
        if label_node is not None:
            operator_node.nodes.append(label_node)
        operator_node.nodes.append(unlabelled_node)

        return operator_node

    def is_unlabelled(self):
        unlabelled_functions = [self.is_compound, self.is_assignment, self.is_adduction,
                                self.is_transition, self.is_conditional, self.is_cycle,
                                self.is_input, self.is_output, self.is_empty, self.is_call
                                ]
        if self.in_cycle and self.token.lexeme == self.SpecialWords['break']:
            self.get_next_lexeme()
            return Tree(tag='break', num_str=self.token.row)
        elif not self.in_cycle and self.token.lexeme == self.SpecialWords['break']:
            raise MyException(self.token.row, 'Unexpected break')
        for func in unlabelled_functions:
            unlabelled_node = func()
            if unlabelled_node:
                return unlabelled_node

        return False

    def is_empty(self):
        if self.token.lexeme in self.IDWordsAndSymbolAfterOperator:
            return Tree(tag='empty', num_str=self.token.row)
        return False

    def is_transition(self):
        if self.token.lexeme != self.SpecialWords['goto']:
            return False
        goto_node = Tree(tag='goto', num_str=self.token.row)
        self.get_next_lexeme()

        if self.token.lexeme != self.IdentifiersLexemes['int']:
            raise MyException(self.token.row, 'Expected label')
        goto_node.attributes.append(Tree(tag='label', value=self.token.value, num_str=self.token.row))
        self.get_next_lexeme()

        return goto_node

    def is_input(self):
        if self.token.lexeme != self.SpecialWords['read']:
            return False
        read_node = Tree(tag='read', num_str=self.token.row)
        expected_variable = True
        while expected_variable:
            self.get_next_lexeme()
            variable_node = self.is_variable()
            if not variable_node:
                raise MyException(self.token.row, 'Expected variable')
            read_node.nodes.append(variable_node)

            if self.token.lexeme != self.SpecialSymbols[',']:
                expected_variable = False
        return read_node

    def is_output(self):
        if self.token.lexeme != self.SpecialWords['write']:
            return False
        write_node = Tree(tag='write', num_str=self.token.row)
        expected_argument = True
        while expected_argument:
            self.get_next_lexeme()
            argument_node = self.is_qualifier()
            if argument_node:
                self.get_next_lexeme()
            else:
                argument_node = self.is_expression()
                if not argument_node:
                    raise MyException(self.token.row, 'Expected qualifier|expression')
            write_node.nodes.append(argument_node)
            if self.token.lexeme != self.SpecialSymbols[',']:
                expected_argument = False
        return write_node

    def is_variable(self):
        if self.token.lexeme != self.IdentifiersLexemes['id']:
            return False
        variable_node = Tree(tag='var', num_str=self.token.row)
        variable_node.attributes.append(Tree(tag='name', value=self.token.value, num_str=self.token.row))
        self.get_next_lexeme()
        if self.token.lexeme == self.SpecialSymbols['[']:
            self.get_next_lexeme()
            index_node = self.is_index()
            if not index_node:
                raise MyException(self.token.row, 'Expected index')
            variable_node.attributes.append(index_node)
            self.get_next_lexeme()
            if self.token.lexeme != self.SpecialSymbols[']']:
                raise MyException(self.token.row, 'Expected "]"')
            self.get_next_lexeme()
        return variable_node

    def is_index(self):
        if self.token.lexeme in (self.IdentifiersLexemes['id'],
                             self.IdentifiersLexemes['int']):
            return Tree(tag='index', value=self.token.value, num_str=self.token.row)
        return False

    def is_qualifier(self):
        if self.token.lexeme in self.QualifierWords.values():
            qualifier_node = Tree(tag='qualifier', num_str=self.token.row)
            qualifier_node.attributes.append(Tree(tag='kind', value=self.token.value, num_str=self.token.row))
            return qualifier_node
        return False

    #################################################################self.SpecialSymbols['[']

    def is_assignment(self):
        if self.token.lexeme != self.SpecialSymbols['(']:
            return False
        checkpoint = self.num_lexeme
        self.get_next_lexeme()
        assign_node = Tree(tag='assign', num_str=self.token.row)

        expression_node = self.is_expression()
        if not expression_node:
            self.get_previous_lexeme(checkpoint)
            return False
        assign_node.nodes.append(expression_node)

        variable_node = self.is_variable()
        if not variable_node:
            self.get_previous_lexeme(checkpoint)
            return False
        assign_node.nodes.append(variable_node)

        if self.token.lexeme != 'Let':
            self.get_previous_lexeme(checkpoint)
            return False
        self.get_next_lexeme()

        if self.token.lexeme != self.SpecialSymbols[')']:
            raise MyException(self.token.row, 'Expected ")"')
        self.get_next_lexeme()

        return assign_node

    def is_expression(self):
        if self.token.lexeme == self.SpecialSymbols['(']:
            expression_node = Tree(tag='op', num_str=self.token.row)
            self.get_next_lexeme()
            first_operand = self.token

            operand_node = self.is_operand()
            if not operand_node:
                raise MyException(self.token.row, 'Expected operand')
            expression_node.nodes.append(operand_node)

            if self.token.lexeme != 'Min':
                second_operand = self.token
                operand_node = self.is_operand()
                if not operand_node:
                    raise MyException(self.token.row, 'Expected operand')
                if self.token.lexeme == 'Mod' and (first_operand.lexeme == 'Real' or second_operand.lexeme == 'Real'):
                    raise MyException(self.token.row, 'Real number is forbidden for mod operation')
                expression_node.nodes.append(operand_node)

            if self.token.lexeme not in self.MathOperations:
                raise MyException(self.token.row, 'Expected operation')
            kind_node = Tree(tag='kind', value=self.token.lexeme, num_str=self.token.row)
            expression_node.attributes.append(kind_node)
            self.get_next_lexeme()

            if self.token.lexeme != self.SpecialSymbols[')']:
                raise MyException(self.token.row, 'Expected ")"')
            self.get_next_lexeme()
        else:
            if self.in_operand:
                self.in_operand = False
                return False
            checkpoint = self.num_lexeme
            expression_node = self.is_operand()
            if not expression_node:
                self.get_previous_lexeme(checkpoint)
                return False

        return expression_node

    def is_operand(self):
        operand_funcs = (self.is_variable, self.is_number, self.is_expression)
        self.in_operand = True
        for func in operand_funcs:
            op_node = func()
            if op_node:
                self.in_operand = False
                return op_node
        self.in_operand = False
        return False

    def is_adduction(self):
        if self.token.lexeme != self.SpecialSymbols['(']:
            return False
        checkpoint = self.num_lexeme
        self.get_next_lexeme()
        variables = []

        variable_node = self.is_variable()
        if not variable_node:
            self.get_previous_lexeme(checkpoint)
            return False
        variables.append(variable_node)

        variable_node = self.is_variable()
        if not variable_node:
            self.get_previous_lexeme(checkpoint)
            return False
        variables.append(variable_node)

        if self.token.lexeme != self.SpecialWords['cast']:
            self.get_previous_lexeme(checkpoint)
            return False
        self.get_next_lexeme()

        if self.token.lexeme != self.SpecialSymbols[')']:
            raise MyException(self.token.row, 'Expected ")"')
        self.get_next_lexeme()

        cast_node = Tree(tag='cast', num_str=self.token.row)
        for var in variables:
            cast_node.nodes.append(var)
        return cast_node

    def is_number(self):
        if self.token.lexeme in (self.IdentifiersLexemes['int'], self.IdentifiersLexemes['real']):
            number_node = Tree(tag=self.token.type, num_str=self.token.row)
            number_node.attributes.append(Tree(tag='val', value=self.token.recval, num_str=self.token.row))
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
        if self.token.lexeme != self.SpecialWords['case']:
            return False
        start_line = self.token.row
        self.get_next_lexeme()
        conditional_tree = Tree(tag='case', num_str=self.token.row)

        expression_node = self.is_expression()
        if not expression_node:
            raise MyException(self.token.row, 'Expected expression')
        conditional_tree.nodes.append(expression_node)

        if self.token.lexeme != self.SpecialWords['of']:
            raise MyException(self.token.row, 'Expected of')
        of_node = Tree(tag='of', num_str=self.token.row)
        self.get_next_lexeme()

        lbls = list()
        if self.token.lexeme != 'Label':
            raise MyException(self.token.row, 'Expected int:')
        number_node = Tree(tag='int', num_str=self.token.row)
        number_node.attributes.append(Tree(tag='val', value=self.token.value[:-1], num_str=self.token.row))
        of_node.nodes.append(number_node)
        lbls.append(self.token.value[:-1])
        self.get_next_lexeme()

        unlabelled_node = self.is_unlabelled()
        if not unlabelled_node:
            raise MyException(self.token.row, 'Expected operator')
        of_node.nodes.append(unlabelled_node)
        conditional_tree.nodes.append(of_node)

        while self.token.lexeme == self.SpecialWords['or']:
            or_node = Tree(tag='or', num_str=self.token.row)
            self.get_next_lexeme()

            if self.token.lexeme != 'Label':
                raise MyException(self.token.row, 'Expected int:')
            if self.token.value[:-1] in lbls:
                raise MyException(self.token.row, 'Repeated label name')
            number_node = Tree(tag='int', num_str=self.token.row)
            number_node.attributes.append(Tree(tag='val', value=self.token.value[:-1], num_str=self.token.row))
            or_node.nodes.append(number_node)
            lbls.append(self.token.value[:-1])
            self.get_next_lexeme()

            unlabelled_node = self.is_unlabelled()
            if not unlabelled_node:
                raise MyException(self.token.row, 'Expected operator')
            or_node.nodes.append(unlabelled_node)
            conditional_tree.nodes.append(or_node)

        while self.token.lexeme == self.SpecialWords['else']:
            else_node = Tree(tag='case', num_str=self.token.row)
            self.get_next_lexeme()

            unlabelled_node = self.is_unlabelled()
            if not unlabelled_node:
                raise MyException(self.token.row, 'Expected operator')
            else_node.nodes.append(unlabelled_node)
            conditional_tree.nodes.append(else_node)

            a = self.num_lexeme
            self.get_next_lexeme()
            if self.token.lexeme != self.SpecialWords['else']:
                self.get_previous_lexeme(a)

        return conditional_tree
    #################################################################
    
    def is_cycle(self):
        if self.token.lexeme != self.SpecialWords['loop']:
            return False
        cycle_tree = Tree(tag='for', num_str=self.token.row)
        self.get_next_lexeme()

        if not self.in_cycle:
            change_in_cycle = True
            self.in_cycle = True
        else:
            change_in_cycle = False

        unlabelled_node = self.is_unlabelled()
        if not unlabelled_node:
            raise MyException(self.token.row, 'Expected unlabelled')
        cycle_tree.nodes.append(unlabelled_node)

        if change_in_cycle:
            self.in_cycle = False

        return cycle_tree
    #################################################################
    
    def is_proc(self):
        if self.token.lexeme != self.SpecialWords['proc']:
            return False
        self.get_next_lexeme()
        if self.token.lexeme != self.IdentifiersLexemes['id']:
            raise MyException(self.token.row, 'Expected id')

        proc_tree = Tree(tag='proc', num_str=self.token.row)
        id_node = Tree(tag='var', num_str=self.token.row)
        id_node.attributes.append(Tree(tag='name', value=self.token.value, num_str=self.token.row))
        proc_tree.nodes.append(id_node)
        self.get_next_lexeme()

        description_node = self.is_description()
        if description_node:
            proc_tree.nodes.append(description_node)
            while self.token.lexeme == self.SpecialSymbols[';']:
                self.get_next_lexeme()
                description_node = self.is_description()
                if not description_node:
                    raise MyException(self.token.row, 'Expected description')
                proc_tree.nodes.append(description_node)

        component_node = self.is_compound()
        if not component_node:
            raise MyException(self.token.row, 'Expected component')
        proc_tree.nodes.append(component_node)

        return proc_tree
    #################################################################
    
    def is_call(self):
        if self.token.lexeme != self.SpecialWords['call']:
            return False

        self.get_next_lexeme()
        if self.token.lexeme != self.IdentifiersLexemes['id']:
            raise MyException(self.token.row, ' Expected id')

        call_tree = Tree(tag='call', num_str=self.token.row)
        id_node = Tree(tag='var', num_str=self.token.row)
        id_node.attributes.append(Tree(tag='name', value=self.token.value, num_str=self.token.row))
        call_tree.nodes.append(id_node)
        self.get_next_lexeme()

        variable_node = self.is_variable()
        while variable_node:
            call_tree.nodes.append(variable_node)
            if self.token.lexeme != self.SpecialSymbols[',']:
                break
            self.get_next_lexeme()
            variable_node = self.is_variable()
            if not variable_node:
                raise MyException(self.token.row, ' Expected variable')

        if self.token.lexeme != self.SpecialWords['end']:
            raise MyException(self.token.row, 'Expected end')

        self.get_next_lexeme()

        return call_tree

    def output_tree(self, tree, n):
        self.tree.write('\t'*n + '<' + tree.tag)
        # if tree.num_str != 0:
        #    self.tree.write(str(tree.num_str))
        if tree.value is not None:
            self.tree.write('="'+tree.value+'"')
        for atr in tree.attributes:
            self.tree.write(' ' + atr.tag + '="' + atr.value + '"')
        if len(tree.nodes) == 0:
            self.tree.write('/>\n')
        else:
            self.tree.write('>\n')
            for i in tree.nodes:
                self.output_tree(i, n+1)
            self.tree.write('\t'*n + '</' + tree.tag + '>' + '\n')


if __name__ == '__main__':
    parser = Parser()
    parser.parsing()
