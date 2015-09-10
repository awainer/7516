'''
Created on 23/8/2015

@author: ari
'''

import logging


class Parser():
    def __init__(self, scanner):
        self.scanner = scanner
        self.tokens = scanner.tokens
        self.log = logging.getLogger('parser')
        if not len(self.log.handlers):
            self.log.setLevel(logging.DEBUG)
            hdlr = logging.FileHandler('/tmp/myapp.log')
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(formatter)
            self.log.addHandler(hdlr)

    def read_token(self):
        self.next_token = self.scanner.next_token()
        self.log.info("Se lee token %s" % self.next_token)
        print("Se lee token %s" % self.next_token)

    def parse(self, debug=0):
        self.log.info("****************************")
        self.log.info("Empezando parse")
        self.parse_program()
        self.log.info("Fin parse")
        return True

    def error(self, s):
        raise ValueError(s)

    def error_expected(self, expected):
        raise ValueError("Se espèraba %s se recibio %s" % (expected, self.next_token))

    def parse_program(self):
        self.read_token()
        self.parse_block()
        if not self.next_token.type == 'program_end':
            self.error("Se esperaba punto, se obtuvo: " + str(self.next_token))

    def parse_const_decl(self):
        last_id = ''
        while self.next_token.type != "semicolon":
            self.read_token()
            if self.next_token.type == "ident":
                last_id = self.next_token.value
                self.log.info("Declaro constante " + self.next_token.value)
                last_id = self.next_token.value
            elif self.next_token.type == "comma":
                pass
            elif self.next_token.type == "equal":
                self.read_token()
                if self.next_token.type == "number":
                    self.log.info("Inicializo  constante %s con %s" % (last_id,
                                                                       self.next_token.value))
                else:
                    self.error("Se esperaba un numero, pero se encontro:" +
                               self.next_token.type)
            elif self.next_token.type == 'semicolon':
                self.read_token()
                return
            else:
                self.error("Error, token inesperado: " + str(self.next_token))

    def assert_type(self, expected_type):
        if not self.next_token.type == type:
            self.error_expected(expected_type)

    def parse_var_decl(self):
        last_id = ''
        while self.next_token.type != "semicolon":
            self.read_token()
            if self.next_token.type == "ident":
                last_id = self.next_token.value
                self.log.info("Declaro variable " + self.next_token.value)
                last_id = self.next_token.value
            elif self.next_token.type == "comma":
                pass
            elif self.next_token.type == "equal":
                self.read_token()
                if self.next_token.type == "number":
                    self.log.info("Inicializo  variable %s con %s" % (last_id,
                                                                      self.next_token.value))
                else:
                    self.error("Se esperaba un numero, pero se encontro:" +
                               self.next_token.type)
            elif self.next_token.type == 'semicolon':
                self.read_token()
                return
            else:
                self.error("Error, token inesperado: " + str(self.next_token))

    def parse_procedure_decl(self):
        self.read_token()
        self.assert_type('ident')
        self.log.info("Parseando procedimiento: %s" % self.next_token.value)
        self.read_token()
        self.assert_type('semicolon')
        self.read_token()
        self.parse_block()
        self.assert_type('semicolon')
        self.read_token()

    def parse_block(self):
        self.log.debug('Parseando bloque')
        if self.next_token.type == 'const':
            self.parse_const_decl()

        if self.next_token.type == 'var':
            self.parse_var_decl()

        while self.next_token.type == 'procedure':
            self.parse_procedure_decl()

        self.parse_statement()
        self.log.debug('Fin parseando bloque')

    def parse_statement(self):
        if self.next_token.type == 'ident':
            self.read_token()
            # last_id = self.last_token.value
            self.assert_type('assign')
            self.read_token()
            self.read_token()
            self.parse_expression()

        elif self.next_token.type == 'call':
            self.read_token()
            self.assert_type('ident')

        elif self.next_token.type == 'begin':
            self.read_token()
            self.parse_statement()
            while not self.next_token.type == 'end':
                self.assert_type('semicolon')
                self.read_token()
                self.parse_statement()

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

    def parse_factor(self):
        if self.next_token.type == 'ident':
            self.read_token()
            return
        if self.next_token.type == 'number':
            self.read_token()
            return
        if self.next_token.type == 'open_parenthesis':
            self.read_token()
            self.parse_expression()
            self.read_token()
            self.assert_type('close_parenthesis')
            self.read_token()

    def parse_term(self):
        self.parse_term()
        while self.next_token.type == 'multiply' or 'divide':
            # TODO ver que op es
            self.read_token()
            self.parse_factor()
        self.read_token()

    def parse_expression(self):
        pass

    def parse_condition(self):
        pass



