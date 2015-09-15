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

class SymbolTable(object):

    CONST = np.uint32(0)
    VAR = np.uint32(1)
    PROCEDURE = np.uint32(2)

    def __init__(self):
        self. table = []
        
    def add_const(self, ident, value, initial_offset):
        self.table.append(Symbol(id, np.uint32(value), self.CONST))

    def add_var(self, ident, value, initial_offset):
        self.table.append(Symbol(id, np.uint32(value), self.VAR))
        
    def add_procedure(self, ident, value, initial_offset):
        self.table.append(Symbol(id, np.uint32(value), self.PROCEDURE))

    
    def lookup(self, ident, finish_position):
        current_position = len(self.table) - 1
        # que lindo sería un do...while
        while True:
            if self.table[current_position].ident == ident:
                return self.table[current_position].ident
            current_position -= 1
            if current_position == 0 or current_position == finish_position:
                return None