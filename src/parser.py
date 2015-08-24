'''
Created on 23/8/2015

@author: ari
'''
from ply import yacc
import logging

class Parser(object):
    def __init__(self, scanner):
        self.scanner = scanner
        self.tokens = scanner.tokens
        log = logging.getLogger()
        self._parser = yacc.yacc(debug=log, module=self)

    def parse(self):
        self._parser.parse(self.scanner.get_lexer())
        
    def p_program(self, p):
        'program :  block "."'
         
    def p_block(self, p):
        ''' 
        block : [ "const" ident "=" number {"," ident "=" number} ";"]  [ "var" ident {"," ident} ";"]  { "procedure" ident ";" block ";" } statement .
        '''
    def p_statement(self, p):
        ''' statement : [ ident ":=" expression | "call" ident 
              | "?" ident | "!" expression 
              | "begin" statement {";" statement } "end" 
              | "if" condition "then" statement 
              | "while" condition "do" statement ].
        '''
        
    def p_condition(self, p):
        ''' condition :  "odd" expression | expression ("="|"#"|"<"|"<="|">"|">=") expression .
        '''
    def p_expression(self, p):
        ''' expression : [ "+"|"-"] term { ("+"|"-") term}.
        '''
    def p_term(self, p):
        ''' term :  factor {("*"|"/") factor}.
        '''
    def p_factor(self, p):
        ''' factor :  ident | number | "(" expression ")".
        '''

    def p_error(self, p):
        print "Syntax error at '%s'" % p.value        
        
