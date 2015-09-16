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

class SymbolTable(object):

    CONST = np.uint32(0)
    VAR = np.uint32(1)
    PROCEDURE = np.uint32(2)

    def __init__(self):
        self. table = []
    
    def duplicate_ident(self, ident):
        raise ValueError("Error, el identificador %s ya se encuentra definido." % ident)

    def add_const(self, ident, value, initial_offset):
        self.check_defined(ident, initial_offset)
        self.table.append(Symbol(ident, np.uint32(value), self.CONST))

    def add_var(self, ident, value, initial_offset):
        print('Adding var',ident)
        self.check_defined(ident, initial_offset)
        self.table.append(Symbol(ident, np.uint32(value), self.VAR))
        

    def check_defined(self, ident, initial_offset):
        for i in self.table[initial_offset-2:]:
            print('Comparando con ', i)
            if i.ident == ident:
                self.duplicate_ident(ident)

    def add_procedure(self, ident, value, initial_offset):
        self.check_defined(ident, initial_offset)
        self.table.append(Symbol(ident, np.uint32(value), self.PROCEDURE))

    
    def lookup(self, ident, finish_position):
        current_position = len(self.table) - 1
        # que lindo sería un do...while
        while True:
            if self.table[current_position].ident == ident:
                return self.table[current_position].ident
            current_position -= 1
            if current_position == 0 or current_position == finish_position:
                return None
