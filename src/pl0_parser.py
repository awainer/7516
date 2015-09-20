'''
Created on 23/8/2015

@author: ari
'''

import logging
from symbol_table import SymbolTable

class Parser():
    def __init__(self, scanner):
        self.scanner = scanner
        self.tokens = scanner.tokens
        self.log = logging.getLogger('parser')
        self.table = SymbolTable()
        if not len(self.log.handlers):
            self.log.setLevel(logging.DEBUG)
            hdlr = logging.FileHandler('/tmp/myapp.log')
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(formatter)
            self.log.addHandler(hdlr)

    def read_token(self):
        self.next_token = self.scanner.next_token()
        self.log.info("Se lee token %s" % self.next_token)

    def parse(self, debug=0):
        self.log.info("****************************")
        self.log.info("Empezando parse")
        self.parse_program()
        self.log.info("Fin parse")
        return True

    def error(self, s):
        self.log.error(s)
        raise ValueError(s)

    def error_expected(self, expected):
        raise ValueError("Se espèraba %s se recibio %s" % (expected, self.next_token))

    def parse_program(self):
        self.read_token()
        self.parse_block(0)
        if not self.next_token.type == 'program_end':
            self.error("Se esperaba punto, se obtuvo: " + str(self.next_token))

    def parse_const_decl(self, base, offset):
        last_id = ''
        while self.next_token.type != "semicolon":
            self.read_token()
            if self.next_token.type == "ident":
                last_id = self.next_token.value
                self.log.info("Declaro constante " + self.next_token.value)
                last_id = self.next_token.value
            elif self.next_token.type == "equal":
                self.read_token()
                if self.next_token.type == "number":
                    self.log.info("Inicializo  constante %s con %s" % (last_id,
                                                                       self.next_token.value))
                    self.table.add_const(last_id, self.next_token.value)
                    offset+=1
                else:
                    self.error("Se esperaba un numero, pero se encontro:" +
                               self.next_token.type)
            elif self.next_token.type == 'semicolon':
                self.read_token()
                return offset
            else:
                self.error("Error, token inesperado: " + str(self.next_token))
        return offset

    def assert_type(self, expected_type):
        if not self.next_token.type == expected_type:
            self.error_expected(expected_type)

    def parse_var_decl(self, base, offset):
        last_id = ''
        while self.next_token.type != "semicolon":
            self.read_token()
            if self.next_token.type == "ident":
                offset+=1
                last_id = self.next_token.value
                self.log.info("Declaro variable " + self.next_token.value)
                last_id = self.next_token.value
            elif self.next_token.type == "comma":
                self.table.add_var(last_id, 0, base)
            elif self.next_token.type == "equal":
                self.read_token()
                if self.next_token.type == "number":
                    self.log.info("Inicializo  variable %s con %s" % (last_id,
                                                                      self.next_token.value))
                    self.table.add_var(last_id, self.next_token.value, base)
                else:
                    self.error("Se esperaba un numero, pero se encontro:" +
                               self.next_token.type)
            elif self.next_token.type == 'semicolon':
                self.table.add_var(last_id, 0, base)
                self.read_token()
                return offset
            else:
                self.error("Error, token inesperado: " + str(self.next_token))
        return offset

    def parse_procedure_decl(self, base, offset):
        self.read_token()
        self.assert_type('ident')
        self.table.add_procedure(self.next_token.value, 0, offset)
        offset+=1
        self.log.info("Parseando procedimiento: %s" % self.next_token.value)
        self.read_token()
        self.assert_type('semicolon')
        self.read_token()
        self.parse_block(base+offset)
        self.assert_type('semicolon')
        self.read_token()
        return offset

    def parse_block(self, base):
        self.log.debug('Parseando bloque')
        offset = 0
        
        if self.next_token.type == 'const':
            offset = self.parse_const_decl(base, offset)

        if self.next_token.type == 'var':
            offset = self.parse_var_decl(base, offset)

        while self.next_token.type == 'procedure':
            offset = self.parse_procedure_decl(base, offset)

        self.parse_statement()
        self.log.debug('Fin parseando bloque')

    def parse_writeln_args(self):
        if self.next_token.type == 'open_parenthesis':
            self.parse_write_args()

    def parse_write_args(self):
        self.assert_type('open_parenthesis')
        self.read_token()
        if self.next_token.type == 'string':
            self.read_token()
        else:
            self.parse_expression()

        while not self.next_token.type == 'close_parenthesis':
            self.assert_type('comma')
            self.read_token()
            if self.next_token.type == 'string':
                self.read_token()
            else:
                self.parse_expression()         
        self.read_token()

    def parse_statement(self):
        self.log.debug('Parseando statement')
        if self.next_token.type == 'ident':
            self.log.info('Asignando valor a %s' % self.next_token.value)
            self.table.get_var(self.next_token.value)
            self.read_token()
            # last_id = self.last_token.value
            self.assert_type('assign')
            self.read_token()
            self.parse_expression()

        elif self.next_token.type == 'call':
            self.read_token()
            self.assert_type('ident')
            self.log.info('Llamando a %s' % self.next_token.value)
            self.table.get_proc(self.next_token.value)
            self.read_token()

        elif self.next_token.type == 'begin':
            self.read_token()
            self.parse_statement()
            while not self.next_token.type == 'end':
                self.assert_type('semicolon')
                self.read_token()
                self.parse_statement()
            self.read_token()

        elif self.next_token.type == 'if':
            self.read_token()
            self.parse_condition()
            self.assert_type('then')
            self.read_token()
            self.parse_statement()
        elif self.next_token.type == 'while':
            self.read_token()
            self.parse_condition()
            self.assert_type('do')
            self.read_token()
            self.parse_statement()
        elif self.next_token.type == 'write':
            self.read_token()
            self.parse_write_args()
        elif self.next_token.type == 'writeln':
            self.read_token()
            self.parse_writeln_args()
        elif self.next_token.type == 'readln':
            self.read_token()
            self.assert_type('open_parenthesis')
            self.read_token()
            self.assert_type('ident')
            self.log.info('Leyendo en %s' % self.next_token.value)
            self.table.get_var(self.next_token.value)
            self.read_token()
            self.assert_type('close_parenthesis')
            self.read_token()


    def parse_factor(self):
        self.log.debug('Parseando factor')
        if self.next_token.type == 'ident':
            try:
                self.table.get_var(self.next_token.value)
            except ValueError:
                self.table.get_const(self.next_token.value)
            self.read_token()
            return
        if self.next_token.type == 'number':
            self.read_token()
            return
        if self.next_token.type == 'open_parenthesis':
            self.read_token()
            self.parse_expression()
            self.assert_type('close_parenthesis')
            self.read_token()

    def parse_term(self):
        self.log.debug('Parseando termino')
        self.parse_factor()
        while self.next_token.type in ['multiply', 'divide']:
            # TODO ver que op es
            self.read_token()
            self.parse_factor()


    def parse_expression(self):
        self.log.debug("Parseando expression")
        if self.next_token.type == 'add':
            self.read_token()
        elif self.next_token.type == 'substract':
            self.read_token()
        self.parse_term()
        while self.next_token.type == 'substract' or self.next_token.type == 'add':
            self.read_token()
            self.parse_term() 

    def parse_condition(self):
        self.log.debug("Parseando condition")
        if self.next_token.type == 'odd':
            self.read_token()
            self.parse_expression()
        else:
            self.read_token()
            self.parse_expression()
            if self.next_token.type == 'equal':
                pass
            else:
                self.assert_type('relation')            
            self.read_token()
            self.parse_expression()



