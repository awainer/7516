'''
Created on 28 de set. de 2015

@author: ari
'''
import numpy as np
import header

class CodeWriter():
    
    def __init__(self):
        self.code = header.header
        self.code += [0xbf, 0x00, 0x00, 0x00, 0x00]
        self.variable_pointer_location = len(self.code) - 4
        self.jumps = {'=': [0x74,0x05], '<>': [0x75,0x05], '<': [0x7c,0x05], '<=': [0x7e,0x05], '>': [0x7f,0x05], '>=': [0x7d,0x05]}
        self.func_address = {'print_string_ebx_to_edx': 0x170, 
                             'print_newline': 0x180, 
                             'print_int_eax': 0x190, 
                             'exit': 0x300, 
                             'read': 0x310}
    def get_code(self):
        return self.code

    def _int_to_bytes(self, number):
        return list(np.array(np.int32(number)).data.tobytes())
    
    def _int_to_one_byte(self, number):
        return list(np.array(np.int8(number)).data.tobytes())

    def _int_to_bytearray(self, number, size):
        if size == 1:
            return list(np.array(np.int8(number)).data.tobytes())
        elif size == 2:
            return list(np.array(np.int16(number)).data.tobytes())
        elif size == 4:
            return list(np.array(np.int32(number)).data.tobytes())
        else:
            raise ValueError('Arraysize no valido: %s' % size) 
    def mov_edi_literal(self, literal):
        self.code +=  [0xbf] + self._int_to_bytes(literal)
         
    def mov_eax_edi_plus_literal(self, literal):
        self.code +=  [0x8b,0x87] + self._int_to_bytes(literal)

    def mov_eax_literal(self, literal):
        self.code +=  [0xb8] + self._int_to_bytes(literal)
        
    def mov_edi_plus_literal_eax(self, literal):
        self.code +=  [0x89,0x87] + self._int_to_bytes(literal)        

    def mov_ecx_literal(self, literal):
        self.code +=  [0xb9] + self._int_to_bytes(literal)
    
    def mov_edx_literal(self, literal):
        self.code +=  [0xba] + self._int_to_bytes(literal)
        
    def xchg_eax_ebx(self):
        self.code +=  [0x93]
    
    def push_eax(self):
        self.code +=  [0x50]
        
    def pop_eax(self):
        self.code +=  [0x58]
    
    def pop_ebx(self):
        self.code +=  [0x5b]
        
    def add_eax_ebx(self):
        self.code +=  [0x01,0xd8]
                            
    def sub_eax_ebx(self):
        self.code +=  [0x29,0xd8]

    def imul_ebx(self):
        self.code +=  [0xf7,0xeb]

    def idiv_ebx(self):
        self.code +=  [0xf7,0xfb]

    def cdq(self):
        self.code +=  [0x99]

    def neg_eax(self):
        self.code +=  [0xf8,0xd8]

    def test_al(self, literal):
        self.code +=  [0xa8] + self._int_to_one_byte(literal)

    def cmp_ebx_eax(self):
        self.code +=  [0x39,0xc3]

    def je_jz(self, literal):
        self.code +=  [0x74] + self._int_to_one_byte(literal)

    def jne_jnz(self, literal):
        self.code +=  [0x75] + self._int_to_one_byte(literal)

    def jg(self, literal):
        self.code +=  [0x7f] + self._int_to_one_byte(literal)
                
    def jge(self, literal):
        self.code +=  [0x7d] + self._int_to_one_byte(literal)

    def jl(self, literal):
        self.code +=  [0x7c] + self._int_to_one_byte(literal)

    def jle(self, literal):
        self.code +=  [0x7e] + self._int_to_one_byte(literal)

    def jpo(self, literal):
        self.code +=  [0x7b] + self._int_to_one_byte(literal)

    def jmp(self, literal):
        self.code +=  [0xe9] + self._int_to_bytes(literal)
    
    def call(self, literal):
        self.code +=  [0xe8] + self._int_to_bytes(literal)
    
    def ret(self):
        self.code +=  [0xc3]
        
    def add_literals(self,literals):
        self.code += literals
    
    def condition_jump(self,condition):
        self.code += self.jumps.get(condition)
        self.code += [0xe9]
        fixup_pos = len(self.code)
        self.code += [0,0,0,0]
        return fixup_pos

    def get_current_position(self):
        return len(self.code)
    
    def fixup(self,position, value, size):
        value = self._int_to_bytearray(value, size)
        for i in range(size):
            self.code[position+i] = value[i]