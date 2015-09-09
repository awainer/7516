'''
Created on 23/8/2015

@author: ari
'''

import logging
import sys


class Parser():
    def __init__(self, scanner):
        self.scanner = scanner
        self.tokens = scanner.tokens
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)

    def read_token(self):
        self.next_token = self.scanner.next_token()

    def parse(self, debug=0):
        self.log.info("Empezando parse")
        self.read_token()

        return True

    def error(self, s):
        raise ValueError(s)

    def parse_program(self):
        self.parse_block()
        if not self.next_token.type == program_end:
            error("Se esperaba punto")

    def parse_const_decl(self):
        while self.next_token.type != "semicolon":
            self.read_token()
            if self.next_token.type == "ident":
                last_id = self.next_token.value
                self.log.info("Declaro constante " + self.next_token.value)
            elif self.next_token.type == "comma":
                pass
            elif self.next_token.type == "equals":
                self.read_token()
                if self.next_token.type == "number":
                    self.log.info("Inicializo  %s con %s" % (last_id,
                                    self.next_token.value))
                else:
                    self.error("Se esperaba un numero, pero se encontro:"
                    + self.next_token.type)
            else:
                self.error("Error, se esperaba")

    def parse_block(self):
        last_id = ''
        if self.next_token.type == 'const':
            self.parse_const_decl()
        elif self.next_token.type == 'var':
            # declaracion de variables
        else:
            self.parse_statement()

    def parse_statement(self):
        pass
    def parse_factor(self):
        pass
    def parse_term(self):
        pass
    def parse_expression(self):
        pass
    def parse_condition(self):
        pass



