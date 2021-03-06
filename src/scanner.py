from ply import lex


class DummyToken():
    def __init__(self,token_type):
        self.type = token_type
        self.value = '*****DUMMY****'

class Scanner(object):

    # Lista de tokens
    tokens = ["number", "equal", "relation", "comma", "semicolon", "assign", "add", "substract",
              "multiply", "divide", "open_parenthesis", "close_parenthesis", "ident", "string",
              "program_end", "newline", "doublequoted_string"]
    # http://stackoverflow.com/questions/5022129/ply-lex-parsing-problem
    reserved = ['const', 'var', 'procedure', 'call', 'if', 'then', 'while', 'do', 'begin', 'end',
                'odd', 'write', 'writeln', 'readln']
    tokens += reserved

    MIN_INT_VALUE = -2147483648  # -2^31
    MAX_INT_VALUE =  2147483647  # 2^31 - 1
    def __init__(self, src_file, debug=0):
        self.lexer = lex.lex(module=self, debug=debug)
        self.lines = src_file.readlines()
        src_file.seek(0)
        self.lexer.input(src_file.read())
        src_file.close()

        print('0: %s' % self.lines[0][:len(self.lines[0]) - 1])
        self.line_count = 1
        
    def get_lexer(self):
        return self.lexer

    def next_token(self):
        return self.lexer.token()


    # Definicion de tokens
    def t_number(self, t):
        r'\d+'
        t.value = int(t.value)
        if t.value < self.MIN_INT_VALUE or t.value > self.MAX_INT_VALUE:
            print('Valor invalido para un entero con signo de 32 bit: %s' % t.value) 
        return t
    t_const = 'const'
    t_equal = '='
    t_comma = ','
    t_semicolon = ';'
    t_var = "VAR"
    t_procedure = "procedure"
    t_assign = ":="
    t_call = "CALL"
    t_begin = "BEGIN"
    t_end = "END"
    t_if = "IF"
    t_then = "THEN"
    t_while = "WHILE"
    t_do = "DO"
    t_odd = "odd"
    t_relation = r"<>|<=|>=|<|>"
    t_add = "\+"
    t_substract = "-"
    t_multiply = "\*"
    t_divide = "/"
    t_open_parenthesis = "\("
    t_close_parenthesis = "\)"

    def t_ident(self, t):
        r"[a-z|A-Z]\w{0,16}"
        if t.value.lower() in self.reserved:
            t.type = t.value.lower()
        return t
    t_ignore = " \t"
    t_writeln = "writeln"
    t_write = "write"

    def t_string(self, t):
        r"'[^']+'"
        # le saco las comillas
        t.value = t.value.replace("'",'')
        return t
    
    def t_doublequoted_string(self, t):
        r'''"[^"]+"'''
        # le saco las comillas
        print('Advertencia, se encontro string entre comillas dobles, deben usarse comillas simples:' + t.value)
        t.value = t.value.replace('"','')
        t.type = 'string'
        return t

    
    t_program_end = "\."


    def log_current_line(self, t):
        try:
            line = self.lines[t.lexer.lineno]
            line = line[:len(line) - 1]
            print('%s: %s' % (t.lexer.lineno, line))
        except IndexError:
            pass

    def t_newline(self, t):
        r'[\n]'
        self.log_current_line(t)
        t.lexer.lineno += 1  # t.value.count('\n')

    def t_error(self, t):
        #raise TypeError("Unknown text '%s' at %s" % (t.value, t.lexer.lineno))
        print("Error, no se encontraron tokens '%s' at %s" % (t.value, t.lexer.lineno))
        t.lexer.skip(1)



