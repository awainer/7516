'''
Created on 28 de set. de 2015

@author: ari
'''
import numpy as np
import header

class CodeWriter():
    
    def __init__(self):
        self.code = header.header

    def get_code(self):
        return self.code

    def _int_to_bytes(self, number):
        return list(np.array(np.int32(number)).data.tobytes())
   
    def mov_edi_literal(self, literal):
        self.code +=  [0xbf] + self._int_to_bytes(literal)
         
    def mov_eax_edi_plus_literal(self, literal):
        self.code +=  [0x8b,0x87] + self._int_to_bytes(literal)

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
        self.code +=  [0xa8] +  list(np.array(np.int8(literal)).data.tobytes())

    def cmp_ebx_eax(self):
        self.code +=  [0x39,0xc3]

    def je_jz(self, literal):
        self.code +=  [0x74] +  list(np.array(np.int8(literal)).data.tobytes())

    def jne_jnz(self, literal):
        self.code +=  [0x75] +  list(np.array(np.int8(literal)).data.tobytes())

    def jg(self, literal):
        self.code +=  [0x7f] +  list(np.array(np.int8(literal)).data.tobytes())
                
    def jge(self, literal):
        self.code +=  [0x7d] +  list(np.array(np.int8(literal)).data.tobytes())

    def jl(self, literal):
        self.code +=  [0x7c] +  list(np.array(np.int8(literal)).data.tobytes())

    def jle(self, literal):
        self.code +=  [0x7e] +  list(np.array(np.int8(literal)).data.tobytes())

    def jpo(self, literal):
        self.code +=  [0x7b] +  list(np.array(np.int8(literal)).data.tobytes())

    def jmp(self, literal):
        self.code +=  [0xe9] +  + self._int_to_bytes(literal)
    
    def call(self, literal):
        self.code +=  [0xe8] +  + self._int_to_bytes(literal)
    
    def ret(self):
        self.code +=  [0xc3]