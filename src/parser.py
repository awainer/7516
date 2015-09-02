'''
Created on 23/8/2015

@author: ari
'''
import sys
import easyply
from ply import yacc
import logging

class Parser(object):
    def __init__(self, scanner):
        self.scanner = scanner
        self.tokens = scanner.tokens
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(logging.StreamHandler(stream=sys.stdout))


    def parse(self):
        
        easyply.process_all(self)
        self._parser = yacc.yacc(debug=True,debuglog=self.log, module=self)
        self.log.info("Empezando parse")
        return self._parser.parse(lexer=self.scanner.get_lexer(),debug=self.log)
    start = 'program'
    def px_program(self, p):
        'program :  block program_end'
        self.log.info("Parseando program %s" % p[1])
        p[0] = p[1]


    def px_block(self, p):
        ''' 
          block : const_decl var_decl proc_decl statement
        '''
        self.log.info("Parseando block: %s" % p[1:])
        p[0] = p[1:]
    
    def px_const_decl(self, p):
        '''
        const_decl : const const_assignment_list 
                    | 
        '''
        self.log.info("Parseando declaracion de constantes: %s" % p[1:])
        p[0] = p[1:]
        
    def px_const_assignment_list(self, p):
        '''
        const_assignment_list : ident equal number 
                                | const_assignment_list comma const_assignment_list
                                | ident
                                | const_assignment_list ";"   
        '''
        self.log.info("Parseando assigment list: %s" % p[1:])
        p[0] = p[1:]
    
    def px_var_decl(self, p):
        '''
        var_decl : var ident_list
                 |
        '''
        self.log.info("Parseando declaracion de variables: %s" % p[1:])
        p[0] = p[1:]
    
    def px_ident_list(self, p):
        '''
        ident_list : ident
        ident_list : ident_list ";"
        ident_list : ident_list comma ident
        '''
        self.log.info("Parseando lista de ids: %s" % p[1:])
        p[0] = p[1:]
    
    def px_proc_decl(self, p):
        '''
        proc_decl : proc_decl procedure ident ";" block ";"
                    |
        '''
        self.log.info("Parseando declaracion de procedimientos: %s" % p[1:])
        #p[0] = p[1:]
    
    def px_readln_args(self, p):
        '''
        readln_args : open_parenthesis ident close_parenthesis
                    | open_parenthesis ident close_parenthesis ";"
                    |  
        
        '''
    
    def px_statement(self , p):
        '''
        statement : ident assign expression
                    | call ident
                    | begin statement_list end
                    | if condition then statement
                    | while condition do statement
                    | writeln writeln_args
                    | write   writeln_args
                    | readln readln_args  
                    | statement ";"
                    | 
        '''
        self.log.info("Parseando statement: %s" % p[1:])
        p[0] = p[1:]
    
    def px_expr_list(self, p):
        '''
        expr_list : expression
                    | expr_list comma expression
        '''
        p[0] = p[1:]
    def px_writeln_args(self, p):
        '''
        writeln_args : open_parenthesis string close_parenthesis
                       | open_parenthesis string comma expr_list close_parenthesis ";"
                       |
        '''
        self.log.info("Parseando write args: %s" % p[1:])
        p[0] = p[1:]
    def px_statement_list(self, p):
        '''
        statement_list : statement 
                        | statement_list ";" statement
                        | statement_list statement
        '''
        self.log.info("Parseando statement list: %s" % p[1:])
        p[0] = p[1:]

    def px_condition(self, p):
        '''
        condition : odd expression
                    | expression relation expression
                    | expression equal expression
        '''
        self.log.info("Parseando condition: %s" % p[1:])
        p[0] = p[1:]
    
    def px_expression(self, p):
        '''
        expression : term 
                    | add term
                    | substract term 
                    | expression add term
                    | expression substract term
        '''
        self.log.info("Parseando expression: %s" % p[1:])
        p[0] = p[1:]
    
    def px_term(self , p):
        '''
        term : factor
               | term multiply factor
               | term divide factor
        '''
        #p = p[0]# [p[1][0], p[2], p[3][0]]
        p[0] = p[1:]
        self.log.info("Parseando term primer : %s" % (p[0]))
        
        
        self.log.info("Parseando term: %s" % p[0])
    
    def px_factor(self, p):
        '''
        factor : ident 
                | number 
                | open_parenthesis expression close_parenthesis
        '''
        p[0] = p[1]
        self.log.info("Parseando factor: %s" % p[0])
    
    def p_error(self, p):
        if not p:
            return
        raise ValueError("Syntax error at '%s' line " % p.value,p.lexer.lineno)        
        
