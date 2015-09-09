'''
Created on 23/8/2015

@author: ari
'''

import logging


class Parser():
    def __init__(self, scanner):
        self.scanner = scanner
        self.tokens = scanner.tokens
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)

    def parse(self, debug=0):
        self.log.info("Empezando parse")
        self.next_token = self.scanner.next_token()
        while tok:
            print(tok.type)
            tok = self.scanner.next_token()
        return True
    
    def parse_program(self):
        self.parse_block()
        assert(self.next_token.type=program_end)
    def parse_block(self):
        if self.next_token.type == 'const':
            # declaracion de constantes
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

    

