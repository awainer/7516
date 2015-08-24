'''
Created on 23/8/2015

@author: ari
'''
from ply import yacc
import logging

class Parser():
    def __init__(self, scanner):
        self.scanner = scanner
        self.tokens = scanner.tokens
        log = logging.getLogger()
        self._parser = yacc.yacc(debug=log, module=self)

    def parse(self):
        self._parser.parse(lexer=self.scanner.get_lexer())
        
    def p_program(self, p):
        'program :  block program_end'


    def p_block(self, p):
        ''' 
          block : const_decl var_decl proc_decl statement
        '''
    def p_const_decl(self, p):
        '''
        const_decl : 
        const_decl : const const_assignment_list 
        '''
            
    def p_const_assignment_list(self, p):
        '''
        const_assignment_list : ident equal number 
                                | const_assignment_list "," ident equal  number    
        '''
        
    def p_var_decl(self, p):
        '''
        var_decl : 
        var_decl : var ident_list 
        '''
    def p_ident_list(self, p):
        '''
        ident_list : ident
        ident_list : ident_list comma ident
        '''
    
    def p_proc_decl(self, p):
        '''
        proc_decl : 
        proc_decl : proc_decl procedure ident semicolon block semicolon
        '''

    def p_statement(self ,p):
        '''
        statement :
        statement : ident assign expression
                    | call ident
                    | begin statement_list end
                    | if condition then statement
                    | while condition do statement
        '''
    def p_statement_list(self, p):
        '''
        statement_list : statement 
                        | statement_list semicolon statement
        '''
    def p_condition(self, p):
        '''
        condition : odd expression
                    | expression relation expression
        '''
    def p_expression(self, p):
        '''
        expression : term 
                    | add term
                    | substract term 
                    | expression add term
        '''
    def p_term(self ,p):
        '''
        term : factor
               | term multiply factor
               | term divide factor
        '''
    
    def p_factor(self, p):
        '''
        factor : ident 
                | number 
                | open_parenthesis expression close_parenthesis
        '''
        
    
    def p_error(self, p):
        print "Syntax error at '%s'" % p.value        
        
