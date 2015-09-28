'''
Created on 13 de set. de 2015

@author: ari
'''
import numpy as np
import logging


class SymbolTable(object):

    CONST = np.uint32(0)
    VAR = np.uint32(1)
    PROCEDURE = np.uint32(2)

    
    
    def __init__(self):
        self.reset()
        self.log = logging.getLogger('parser')
        if not len(self.log.handlers):
            self.log.setLevel(logging.DEBUG)
            hdlr = logging.FileHandler('/tmp/myapp.log')
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(formatter)
            self.log.addHandler(hdlr)

    def __repr__(self):
        return str(self.table)
    
    def __str__(self, *args, **kwargs):
        return self.__repr__()

    def reset(self):
        self. table = []

    def duplicate_ident(self, ident):
        raise ValueError("Error, el identificador %s ya se encuentra definido." % ident)

    def add_const(self, ident, value, initial_offset):
        self.check_defined(ident, initial_offset)
        self.table.append(Symbol(ident.strip(), np.uint32(value), self.CONST))

    def add_var(self, ident, value, initial_offset):
        print('Adding var',ident)
        self.check_defined(ident, initial_offset)
        self.table.append(Symbol(ident.strip(), np.uint32(value), self.VAR))
        
    def add_procedure(self, ident, value, initial_offset):
        self.check_defined(ident, initial_offset)
        self.table.append(Symbol(ident.strip(), np.uint32(value), self.PROCEDURE))

    ## TODO ver base
    def check_defined(self, ident, base):
        scope = self.table[base:]
        print('Buscando %s en scope (base %s) : %s' % (ident, base,scope))
        for i in scope:
            print('Comparando con ', i)
            if i.ident == ident:
                self.duplicate_ident(ident)

    def _get_symbol(self, ident, id_type, base, offset):
        self.log.debug("Get symbol: %s base %s, offset %s " % (ident,base,offset))
        end = 0
        start = base + offset - 1
        res = self.lookup(ident.strip(),start, end)
        if not res:
            raise ValueError("Identificador desconocido: %s" % ident)
        
        if res.type == id_type:
            return res
        else:
            raise ValueError("Identificador %s de tipo incorrecto, se obtuvo: %s y se esperaba %s" % (ident, res.types[res.type], res.types[id_type]))

    def get_var(self, ident, base, offset):
        return self._get_symbol(ident, self.VAR, base, offset)

    def get_const(self, ident, base, offset):
        return self._get_symbol(ident, self.CONST, base, offset )

    def get_proc(self, ident,base, offset):
        return self._get_symbol(ident, self.PROCEDURE, base, offset)    
            
    def lookup(self, ident,start,end):
        current_position = start
        print('Lookup (%s)start: %s end: %s' % (ident,start,end))
        print('Lookup Table (size %s): %s' % (len(self.table),self.table))
        print('Buscando en %s' % self.table[end:start])
        while True and current_position >= end:
            if self.table[current_position].ident == ident:
                return self.table[current_position]
            current_position -= 1
        return None
    
class Symbol(object):
    types = { SymbolTable.CONST: 'Const', SymbolTable.VAR: 'Var', SymbolTable.PROCEDURE: 'Procedure'}
    
    def __init__(self, ident, value, symbol_type):
        self.value = value
        self.ident = ident
        self.type = symbol_type
    
    def __str__(self):
        return str(self.ident) + '=' + str(self.value) + ' tipo: ' + self.types[self.type]
    
    def __repr__(self):
        return self.__str__()    
