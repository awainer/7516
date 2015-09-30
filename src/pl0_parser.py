'''
Created on 23/8/2015

@author: ari
'''

import logging
from symbol_table import SymbolTable
from code_writer import CodeWriter

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
        self.writer = CodeWriter()

    
    def read_token(self):
        self.next_token = self.scanner.next_token()
        self.log.info("Se lee token %s" % self.next_token)

    def parse(self, debug=0):
        self.log.info("****************************")
        self.log.info("Empezando parse")
        try:
            self.parse_program()
        except ValueError as e:
            print('Ultimo token %s' %(self.next_token))
            raise e
        self.log.info("Fin parse")
        return True

    def error(self, s):
        self.log.error(s)
        raise ValueError(s)

    def error_expected(self, expected):
        raise ValueError("Se esperaba %s se recibio %s" % (expected, self.next_token))

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
                    self.table.add_const(last_id, self.next_token.value, base)
                    offset+=1
                    self.read_token()
                    if self.next_token.type == 'comma':
                        pass
                        #self.read_token()
                else:
                    self.error("Se esperaba un numero, pero se encontro:" +
                               self.next_token.type)
            elif self.next_token.type == 'semicolon':
                self.read_token()
                return offset
            else:
                self.error("Error, token inesperado: " + str(self.next_token))
        self.read_token()
        return offset

    def assert_type(self, expected_type):
        if not self.next_token.type == expected_type:
            self.error_expected(expected_type)

    def parse_var_decl(self, base, offset):
        last_id = ''
        added=False
        while self.next_token.type != "semicolon":
            self.read_token()
            if self.next_token.type == "semicolon":
                if not added:
                    self.table.add_var(last_id, base)
                self.read_token()
                break
            elif self.next_token.type == "ident":
                offset+=1
                last_id = self.next_token.value
                added = False
                self.log.info("Declaro variable " + self.next_token.value)
            elif self.next_token.type == "comma":
                self.table.add_var(last_id, base)
                added = True
                self.log.info("Inicializo  variable %s con valor por defecto" % last_id)
            #----------------------------- elif self.next_token.type == "equal":
                #--------------------------------------------- self.read_token()
                #-------------------------- if self.next_token.type == "number":
                    # self.log.info("Inicializo  variable %s con %s" % (last_id,
                                                                      # self.next_token.value))
                    #-- self.table.add_var(last_id, self.next_token.value, base)
                    #---------------------------------------------- added = True
            #------------------------------------------------------------- else:
                #------- self.error("Se esperaba un numero, pero se encontro:" +
                               #-------------------------- self.next_token.type)
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
        self.table.add_procedure(self.next_token.value, 0, base)
        #offset+=1        
        self.log.debug("Agrego proc %s, base %s offset %s" % (self.next_token.value,base,offset))
        self.log.info("Parseando procedimiento: %s" % self.next_token.value)
        self.read_token()
        self.assert_type('semicolon')
        self.read_token()
        self.parse_block(base+offset)
        self.assert_type('semicolon')
        self.read_token()
        return offset

    def parse_block(self, base):
        self.log.debug('Parseando bloque, base: ' + str(base))
        offset = 0
        
        if self.next_token.type == 'const':
            offset = self.parse_const_decl(base, offset)

        if self.next_token.type == 'var':
            offset = self.parse_var_decl(base, offset)

        while self.next_token.type == 'procedure':
            offset+=1
            self.parse_procedure_decl(base, offset)

        self.parse_statement(base, offset)
        self.log.debug('Fin parseando bloque, base %s offset %s' % (base,offset))
        return offset;

    def parse_writeln_args(self, base, offset):
        if self.next_token.type == 'open_parenthesis':
            self.parse_write_args(base, offset)

    def parse_write_args(self,base, offset):
        self.assert_type('open_parenthesis')
        self.read_token()
        if self.next_token.type == 'string':
            self.read_token()
        else:
            self.parse_expression(base, offset)

        while not self.next_token.type == 'close_parenthesis':
            self.assert_type('comma')
            self.read_token()
            if self.next_token.type == 'string':
                self.read_token()
            else:
                self.parse_expression(base, offset)         
        self.read_token()

    def parse_statement(self, base, offset):
        self.log.debug('Parseando statement')
        if self.next_token.type == 'ident':
            self.log.info('Asignando valor a %s' % self.next_token.value)
            self.table.get_var(self.next_token.value, base, offset)
            self.read_token()
            # last_id = self.last_token.value
            self.assert_type('assign')
            self.read_token()
            self.parse_expression(base, offset)

        elif self.next_token.type == 'call':
            self.read_token()
            self.assert_type('ident')
            self.log.info('Llamando a %s' % self.next_token.value)
            self.table.get_proc(self.next_token.value,base,offset)
            self.read_token()

        elif self.next_token.type == 'begin':
            self.read_token()
            self.parse_statement(base, offset)
            while not self.next_token.type == 'end':
                self.assert_type('semicolon')
                self.read_token()
                self.parse_statement(base, offset)
            self.read_token()

        elif self.next_token.type == 'if':
            self.read_token()
            fixup_pos = self.parse_condition(base, offset)
            self.assert_type('then')
            self.read_token()
            self.parse_statement(base, offset)
            self.writer.fixup(fixup_pos,self.writer.get_current_position())
        elif self.next_token.type == 'while':
            self.read_token()
            fixup_pos = self.parse_condition(base, offset)
            self.assert_type('do')
            self.read_token()
            self.parse_statement(base, offset)
            self.writer.fixup(fixup_pos,self.writer.get_current_position())
        elif self.next_token.type == 'write':
            self.read_token()
            self.parse_write_args(base, offset)
        elif self.next_token.type == 'writeln':
            self.read_token()
            self.parse_writeln_args(base, offset)
        elif self.next_token.type == 'readln':
            self.read_token()
            self.assert_type('open_parenthesis')
            self.read_token()
            self.assert_type('ident')
            self.log.info('Leyendo en %s' % self.next_token.value)
            self.table.get_var(self.next_token.value, base, offset)
            self.read_token()
            self.assert_type('close_parenthesis')
            self.read_token()


    def parse_factor(self, base, offset):
        self.log.debug('Parseando factor')
        if self.next_token.type == 'ident':
            try:
                arg = self.table.get_var(self.next_token.value, base, offset)
                self.writer.mov_eax_edi_plus_literal(arg.value)
                self.writer.push_eax()
            except ValueError:
                arg = self.table.get_const(self.next_token.value, base, offset)
                self.writer.mov_eax_literal(arg.value)
                self.writer.push_eax()
                
            self.read_token()
            return
        if self.next_token.type == 'number':
            self.writer.mov_eax_literal(self.next_token.value)
            self.writer.push_eax()
            
            self.read_token()
            return
        if self.next_token.type == 'open_parenthesis':
            self.read_token()
            self.parse_expression(base, offset)
            self.assert_type('close_parenthesis')
            self.read_token()

    def parse_term(self,base, offset):
        self.log.debug('Parseando termino')
        self.parse_factor(base, offset)
        while self.next_token.type in ['multiply', 'divide']:
            last_op = self.next_token.type 
            # TODO ver que op es
            self.read_token()
            self.parse_factor(base, offset)
            if last_op == 'multiply':
                self.writer.pop_eax()
                self.writer.pop_ebx()
                self.writer.imul_ebx()
                self.writer.push_eax()
            elif last_op == 'divide':
                self.writer.add_literals([0x58,0x5b,0x93,0x99,0xf7,0xfb,0x50]) # TODO pasar esto a asm
            else:
                raise ValueError('term must be a multiply or divide operation')


    def parse_expression(self, base, offset):
        self.log.debug("Parseando expression")
        unary_minus = False
        if self.next_token.type == 'substract':
            unary_minus = True
            self.read_token()
        self.parse_term(base, offset)
        if unary_minus:
            self.writer.pop_eax()
            self.writer.neg_eax()
            self.writer.push_eax()
        while self.next_token.type == 'substract' or self.next_token.type == 'add':
            last_op = self.next_token.type
            self.read_token()
            self.parse_term(base, offset) 
            if last_op == 'add':
                self.writer.pop_eax()
                self.writer.pop_ebx()
                self.writer.add_eax_ebx()
                self.writer.push_eax()
            elif last_op == 'substract':
                self.writer.add_literals([0x58,0x5b,0x93,0x29,0xd8,0x50])

    def parse_condition(self, base, offset):
        
        self.log.debug("Parseando condition")
        if self.next_token.type == 'odd':
            self.read_token()
            self.parse_expression(base, offset)
            self.writer.add_literals([0x58, 0xa8, 0x01, 0x7b, 0x05, 0xe9, 0x00, 0x00, 0x00, 0x00])
            fixup_pos = self.writer.get_current_position() - 4
        else:
            self.read_token()
            self.parse_expression(base, offset)
            
            if self.next_token.type == 'equal':
                last_rel = '='
            else:
                self.assert_type('relation')
                last_rel = self.next_token.value            
            self.read_token()
            self.parse_expression(base, offset)
            self.writer.add_literals([0x58,0x5b,0x39,0xc3])
            fixup_pos = self.writer.condition_jump(last_rel)
        return fixup_pos


