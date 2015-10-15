

class NullWriter():
            
    def get_code(self):
        return []

    def flush(self, variable_count):
        pass

    def mov_edi_literal(self, literal):
        pass
         
    def mov_eax_edi_plus_literal(self, literal):
        pass
    
    def mov_eax_literal(self, literal):
        pass
            
    def mov_edi_plus_literal_eax(self, literal):
        pass
    
    def mov_ecx_literal(self, literal):
        pass
        
    def mov_edx_literal(self, literal):
        pass
            
    def xchg_eax_ebx(self):
        pass
    
    def push_eax(self):
        pass
            
    def pop_eax(self):
        pass
        
    def pop_ebx(self):
        pass
            
    def add_eax_ebx(self):
        pass
                                
    def sub_eax_ebx(self):
        pass
    
    def imul_ebx(self):
        pass
    
    def idiv_ebx(self):
        pass
    
    def cdq(self):
        pass
    
    def neg_eax(self):
        pass
    
    def test_al(self, literal):
        pass
    
    def cmp_ebx_eax(self):
        pass
    
    def je_jz(self, literal):
        pass
    
    def jne_jnz(self, literal):
        pass
    
    def jg(self, literal):
        pass
                    
    def jge(self, literal):
        pass
    
    def jl(self, literal):
        pass
    
    def jle(self, literal):
        pass
    
    def jpo(self, literal):
        pass
    
    def jmp(self, literal):
        pass
        
    def call(self, literal):
        pass
        
    def ret(self):
        pass
            
    def add_literals(self, literals):
        pass
        
    def write_newline(self):
        pass
        
    def write_number(self):
        pass
    
    def readln(self):
        pass

    def write_string(self, string):
        pass
    
    def condition_jump(self, condition):
        pass
    
    def get_current_position(self):
        pass
    
    def fixup(self, position, value, size, signed=True):
        pass