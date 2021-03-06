'''
Created on 28 de set. de 2015

@author: ari
'''
import os
import stat
import numpy as np
import header
import logging


class CodeWriter():
    DEFAULT_OUT_FILE = '/tmp/out.elf'
    def __init__(self, out_file=None):
        self.out_file = out_file or self.DEFAULT_OUT_FILE
        self.code = header.header
        self.load_address = 0x8048000
        self.text_section_start = 224  # pagina 22 del apunte
        self.code += [0xbf, 0x00, 0x00, 0x00, 0x00]
        self.variable_pointer_location = len(self.code) - 4
        self.jumps = {'=': [0x74, 0x05], '<>': [0x75, 0x05], '<': [0x7c, 0x05], '<=': [0x7e, 0x05], '>': [0x7f, 0x05], '>=': [0x7d, 0x05], 'odd': [0x7b, 0x05]}
        self.func_address = {'print_string_ebx_to_edx': 0x170,
                             'print_newline': 0x180,
                             'print_int_eax': 0x190,
                             'exit': 0x300,
                             'read': 0x310}

        self.log = logging.getLogger('writer')
        self.log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr = logging.FileHandler('/tmp/writer.log')
        hdlr.setFormatter(formatter)
        self.log.addHandler(hdlr)
        
                
    def get_code(self):
        return self.code

    def flush(self, variable_count):
        

        # salto incondicional a la int que termina el proceso
        # esos 5 son los que ocupa esta instruccion, hay que contar desde ahi 
        self.jmp(0x300 - len(self.code) - 5)

        self.log.info('Fin de parse de codigo, pasando a variables y fixups generales.')
         
        # fixup del puntero a las variables (EDI), salto absoluto
        self.fixup(self.variable_pointer_location, len(self.code) + self.load_address, 4)

        # espacio para las variables
        for _ in range(variable_count):
            self.code += [0, 0, 0, 0]
            self.log.info('Agregando var')
        # FileSize
        self.fixup(68, len(self.code), 4, signed=False)
        # MemorySize
        self.fixup(72, len(self.code), 4, signed=False)
        # Text size
        self.fixup(201, len(self.code) - self.text_section_start , 4, signed=False)
        with open(self.out_file, 'wb') as outfile:
            outfile.write(bytearray(self.code))
        st = os.stat(self.out_file)    
        os.chmod(self.out_file, st.st_mode | stat.S_IEXEC)
        pos = 0
        for i in self.code:
            self.log.warning("Out: offset %s value %s" % (pos, hex(i)))
            pos += 1

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

    def _unsigned_int_to_bytearray(self, number, size):
        if size == 1:
            return list(np.array(np.uint8(number)).data.tobytes())
        elif size == 2:
            return list(np.array(np.uint16(number)).data.tobytes())
        elif size == 4:
            return list(np.array(np.uint32(number)).data.tobytes())
        else:
            raise ValueError('Arraysize no valido: %s' % size) 

    def mov_edi_literal(self, literal):
        self.log.info('[%s] mov edi,%s' % (len(self.code), literal))
        self.code += [0xbf] + self._int_to_bytes(literal)
         
    def mov_eax_edi_plus_literal(self, literal):
        self.log.info('[%s] mov eax,[edi+%s]' % (len(self.code), literal))
        self.code += [0x8b, 0x87] + self._int_to_bytes(literal)

    def mov_eax_literal(self, literal):
        self.log.info('[%s] mov eax,%s' % (len(self.code), literal))
        self.code += [0xb8] + self._int_to_bytes(literal)
        
    def mov_edi_plus_literal_eax(self, literal):
        self.log.info('[%s] mov [edi+%s],eax' % (len(self.code), literal))
        self.code += [0x89, 0x87] + self._int_to_bytes(literal)        

    def mov_ecx_literal(self, literal):
        self.log.info('[%s] mov ecx,%s' % (len(self.code), literal))
        self.code += [0xb9] + self._int_to_bytes(literal)
    
    def mov_edx_literal(self, literal):
        self.log.info('[%s] mov edx,%s' % (len(self.code), literal))
        self.code += [0xba] + self._int_to_bytes(literal)
        
    def xchg_eax_ebx(self):
        self.log.info('[%s] xchg eax,ebx' % len(self.code))
        self.code += [0x93]
    
    def push_eax(self):
        self.log.info('[%s] push eax' % len(self.code))
        self.code += [0x50]
        
    def pop_eax(self):
        if self.code[-1] == 0x50:
            self.code.pop()
            return
        
        self.log.info('[%s] pop eax' % len(self.code))
        self.code += [0x58]
    
    def pop_ebx(self):
        self.log.info('[%s] pop ebx' % len(self.code))
        self.code += [0x5b]
        
    def add_eax_ebx(self):
        self.log.info('[%s] add eax,ebx' % len(self.code))
        self.code += [0x01, 0xd8]
                            
    def sub_eax_ebx(self):
        self.log.info('[%s] sub eax,ebx' % len(self.code))
        self.code += [0x29, 0xd8]

    def imul_ebx(self):
        self.log.info('[%s] imul ebx' % len(self.code))
        self.code += [0xf7, 0xeb]

    def idiv_ebx(self):
        self.log.info('[%s] idiv ebx' % len(self.code))
        self.code += [0xf7, 0xfb]

    def cdq(self):
        self.log.info('[%s] cdq' % len(self.code))
        self.code += [0x99]

    def neg_eax(self):
        self.log.info('[%s] neg  eax' % len(self.code))
        self.code += [0xf7, 0xd8]

    def test_al(self, literal):
        self.log.info('[%s] test al' % len(self.code))
        self.code += [0xa8] + self._int_to_one_byte(literal)

    def cmp_ebx_eax(self):
        self.log.info('[%s] cmp ebx,eax' % len(self.code))
        self.code += [0x39, 0xc3]

    def je_jz(self, literal):
        self.log.info('[%s] je %s' % (len(self.code), literal))
        self.code += [0x74] + self._int_to_one_byte(literal)

    def jne_jnz(self, literal):
        self.log.info('[%s] jne %s' % (len(self.code), literal))
        self.code += [0x75] + self._int_to_one_byte(literal)

    def jg(self, literal):
        self.log.info('[%s] jg %s' % (len(self.code), literal))
        self.code += [0x7f] + self._int_to_one_byte(literal)
                
    def jge(self, literal):
        self.log.info('[%s] jge %s' % (len(self.code), literal))
        self.code += [0x7d] + self._int_to_one_byte(literal)

    def jl(self, literal):
        self.log.info('[%s] jle %s' % (len(self.code), literal))
        self.code += [0x7c] + self._int_to_one_byte(literal)

    def jle(self, literal):
        self.log.info('[%s] jle %s' % (len(self.code), literal))
        self.code += [0x7e] + self._int_to_one_byte(literal)

    def jpo(self, literal):
        self.log.info('[%s] jpo %s' % (len(self.code), literal))
        self.code += [0x7b] + self._int_to_one_byte(literal)

    def jmp(self, literal):
        self.log.info('[%s] jmp %s' % (len(self.code), literal))
        self.code += [0xe9] + self._int_to_bytes(literal)
        return len(self.code) - 4
    
    def call(self, literal):
        self.log.info('[%s] call %s' % (len(self.code), literal))
        self.code += [0xe8] + self._int_to_bytes(literal)
    
    def ret(self):
        self.log.info('[%s] ret' % len(self.code))
        self.code += [0xc3]
        
    def add_literals(self, literals):
        self.code += literals
        
    def write_newline(self):
        self.call(self.func_address['print_newline'] - len(self.code) - 5)
        
    def write_number(self):
        self.pop_eax()
        self.call(self.func_address['print_int_eax'] - len(self.code) - 5)

    def readln(self):
        self.call(self.func_address['read'] - len(self.code) - 5)

    def write_string(self, string):
        string_position = len(self.code) + self.load_address + 20  # 5+5+5
        self.mov_ecx_literal(string_position) 
        self.mov_edx_literal(len(string))  # 5 bytes
        self.call(self.func_address['print_string_ebx_to_edx'] - len(self.code) - 5)  # 5 bytes
        fixup_address = len(self.code) + 1
        self.jmp(0)  # 5 bytes
        self.log.warning("[%s] [%s]" % (len(self.code), [ hex(ord(x)) for x in string ]))
        self.code += [ ord(x) for x in string ]
        self.fixup(fixup_address, len(string), 4)

    def condition_jump(self, condition):
        self.log.info('[%s] %s' % (len(self.code), self.jumps.get(condition)))
        self.code += self.jumps.get(condition)
        self.code += [0xe9]
        fixup_pos = len(self.code)
        self.code += [0, 0, 0, 0]
        return fixup_pos

    def get_current_position(self):
        return len(self.code)
    
    def fixup(self, position, value, size, signed=True):
        if signed:
            value = self._int_to_bytearray(value, size)
        else:
            value = self._unsigned_int_to_bytearray(value, size)
        for i in range(size):
            self.log.warning("Fixup: %s=%s (%s)" % (position + i, value[i], hex(value[i])))
            self.code[position + i] = value[i]

    def delete_last_n_bytes(self,count):
        self.log.info('Borro bytes: ' + str(count))
        self.code = self.code[:len(self.code) - 5]