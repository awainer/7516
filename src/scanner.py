from ply import lex


class Scanner(object):

    # Lista de tokens
    tokens = ["number", "equal", "relation", "comma", "semicolon", "assign", "add", "substract",
              "multiply", "divide", "open_parenthesis", "close_parenthesis", "ident", "string",
              "program_end", "newline", ]
    # http://stackoverflow.com/questions/5022129/ply-lex-parsing-problem
    reserved = ['const', 'var', 'procedure', 'call', 'if', 'then', 'while', 'do', 'begin', 'end',
                'odd', 'write', 'writeln', 'readln']
    tokens += reserved

    def __init__(self, src_file, debug=0):
        self.lexer = lex.lex(module=self, debug=debug)
        self.lines = src_file.readlines()
        src_file.seek(0)
        self.lexer.input(src_file.read())
        src_file.close()
        self.log_line('1', self.lines[0].strip())
        self.line_count = 0
        
    def get_lexer(self):
        return self.lexer

    def next_token(self):
        return self.lexer.token()

    # Definicion de tokens
    def t_number(self, t):
        r'\d+'
        t.value = int(t.value)
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
    t_string = "'.*'"
    t_program_end = "\."

    def t_newline(self, t):
        r'[\n\r]+'
        self.log_current_line(t)
        t.lexer.lineno += t.value.count('\n')

    def log_line(self,number, line):        
        print('***** Reading line %s : %s' %(number, line))

    def log_current_line(self,t):
        while self.line_count < t.lexer.lineno:
            self.log_line(t.lexer.lineno+1, self.lines[self.line_count].strip())
            self.line_count+=1
        #self.log_line(t.lexer.lineno+1, self.lines[t.lexer.lineno].strip())

    def t_error(self, t):
        raise TypeError("Unknown text '%s' at %s" % (t.value, t.lexer.lineno))


