'''
Created on 23/8/2015

@author: ari
'''
import sys
from ply import yacc
import logging


class Parser():
    def __init__(self, scanner):
        self.scanner = scanner
        self.tokens = scanner.tokens
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(logging.StreamHandler(stream=sys.stdout))
        self._parser = yacc.yacc(debug=logging.getLogger(), module=self)

    def parse(self, debug=0):
        self.log.info("Empezando parse")
        return self._parser.parse(lexer=self.scanner.get_lexer(), debug=debug)

    start = 'program'

    def p_program(self, p):
        'program :  block program_end'
        self.log.info("Parseando program %s" % p[1])
        p[0] = p[1]

    def p_block(self, p):
        '''
          block : const_decl var_decl proc_decl
        '''
        self.log.info("Parseando block: %s" % p[1:])
        p[0] = p[1:]

    def p_const_decl(self, p):
        '''
        const_decl : const const_assignment_list
                    |
        '''
        self.log.info("Parseando declaracion de constantes: %s" % p[1:])
        p[0] = p[1:]

    def p_const_assignment_list(self, p):
        '''
        const_assignment_list : ident equal number
                                | const_assignment_list comma const_assignment_list
                                | ident
                                | const_assignment_list semicolon
        '''
        self.log.info("Parseando assigment list: %s" % p[1:])
        p[0] = p[1:]

    def p_var_decl(self, p):
        '''
        var_decl : var ident_list semicolon
                 |
        '''
        self.log.info("Parseando declaracion de variables: %s" % p[1:])
        p[0] = p[1:]

    def p_ident_list(self, p):
        '''
        ident_list : ident
                   | ident_list comma ident
        '''
    def p_proc_decl(self, p):
        '''
        proc_decl : procedure ident semicolon block semicolon
                  |
        '''

    def p_error(self, p):
        if not p:
            return
        raise ValueError("Syntax error at '%s' line " % p.value, p.lexer.lineno)

