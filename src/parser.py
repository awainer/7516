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

    def parse(self):
        self.log.info("Empezando parse")
        self._parser.parse(lexer=self.scanner.get_lexer())
        
    def p_program(self, p):
        'program :  block program_end'
        self.log.info("Parseando program")


    def p_block(self, p):
        ''' 
          block : const_decl var_decl proc_decl statement
        '''
        self.log.info("Parseando block: %s" % p)
    def p_const_decl(self, p):
        '''
        const_decl : 
        const_decl : const const_assignment_list 
        '''
        self.log.info("Parseando declaracion de constantes: %s" % p)    
    def p_const_assignment_list(self, p):
        '''
        const_assignment_list : ident equal number 
                                | const_assignment_list "," ident equal  number    
        '''
        self.log.info("Parseando assigment list: %s" % p)
    def p_var_decl(self, p):
        '''
        var_decl : 
        var_decl : var ident_list 
        '''
        self.log.info("Parseando declaracion de variables: %s" % p)
    def p_ident_list(self, p):
        '''
        ident_list : ident
        ident_list : ident_list comma ident
        '''
        self.log.info("Parseando lista de ids: %s" % p)
    
    def p_proc_decl(self, p):
        '''
        proc_decl : 
        proc_decl : proc_decl procedure ident semicolon block semicolon
        '''
        self.log.info("Parseando declaracion de procedimientos: %s" % p)

    def p_statement(self , p):
        '''
        statement :
        statement : ident assign expression
                    | call ident
                    | begin statement_list end
                    | if condition then statement
                    | while condition do statement
        '''
        self.log.info("Parseando statement: %s" % p)
        
    def p_statement_list(self, p):
        '''
        statement_list : statement 
                        | statement_list semicolon statement
        '''
        self.log.info("Parseando statement list: %s" % p)
    def p_condition(self, p):
        '''
        condition : odd expression
                    | expression relation expression
        '''
        self.log.info("Parseando condition: %s" % p)
    def p_expression(self, p):
        '''
        expression : term 
                    | add term
                    | substract term 
                    | expression add term
        '''
        self.log.info("Parseando expression: %s" % p)
    def p_term(self , p):
        '''
        term : factor
               | term multiply factor
               | term divide factor
        '''
        self.log.info("Parseando term: %s" % p)
    def p_factor(self, p):
        '''
        factor : ident 
                | number 
                | open_parenthesis expression close_parenthesis
        '''
        self.log.info("Parseando factor: %s" % p)
    
    def p_error(self, p):
        print "Syntax error at '%s'" % p.value        
        
