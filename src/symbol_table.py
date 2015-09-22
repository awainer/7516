'''
Created on 13 de set. de 2015

@author: ari
'''
import numpy as np

class Symbol(object):
    
    def __init__(self, ident, value, symbol_type):
        self.value = value
        self.ident = ident
        self.type = symbol_type
    
    def __str__(self):
        return str(self.ident) + '=' + str(self.value) + ' tipo: ' + str(self.type)
    
    def __repr__(self):
        return self.__str__()

class SymbolTable(object):

    CONST = np.uint32(0)
    VAR = np.uint32(1)
    PROCEDURE = np.uint32(2)

    types = { CONST: 'Const', VAR: 'Var', PROCEDURE: 'Procedure'}
    
    def __init__(self):
        self.reset()

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

    def check_defined(self, ident, base):
        scope = self.table[base:]
        print('Buscando %s en scope (base %s) : %s' % (ident, base,scope))
        for i in scope:
            print('Comparando con ', i)
            if i.ident == ident:
                self.duplicate_ident(ident)

    def _get_symbol(self, ident, id_type):
        res = self.lookup(ident.strip())
        if not res:
            raise ValueError("Identificador desconocido: %s" % ident)
        
        if res.type == id_type:
            return res
        else:
            raise ValueError("Identificador de tipo incorrecto, se obtuvo: %s y se esperaba %s" % (self.types[res.type], self.types[id_type]))

    def get_var(self, ident):
        return self._get_symbol(ident, self.VAR)

    def get_const(self, ident):
        return self._get_symbol(ident, self.CONST)

    def get_proc(self, ident):
        return self._get_symbol(ident, self.PROCEDURE)    
            
    def lookup(self, ident):
        current_position = len(self.table) - 1

        while True and current_position >= 0:
            if self.table[current_position].ident == ident:
                return self.table[current_position]
            current_position -= 1
        return None
