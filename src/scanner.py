from ply import lex

class Scanner(object):

    # Lista de tokens
    tokens = ["number", "equal", "not_equal", "comma", "semicolon", "assign", "logic_operation", "add", "substract", "multiply", "divide", "open_parenthesis", "close_parenthesis", "ident", "string", "program_end", "newline", ]
    # http://stackoverflow.com/questions/5022129/ply-lex-parsing-problem
    reserved = [ 'const', 'var', 'procedure', 'call', 'if', 'then', 'while', 'do', 'begin', 'end', 'odd', 'write', 'writeln', 'readln' ]
    tokens += reserved
    
    def __init__(self,src_file):
        self.lexer = lex.lex(module=self)
        text = src_file.read()
        self.lexer.input(text)        

    def get_lexer(self):
        return self.lexer
    
    def next_token(self):
        return self.lexer.token()
    
    # Definicion de tokens
    def t_number(self, t):
        r'\d+'
        t.value = int(t.value)
        return t
    t_const = 'const '
    t_equal = '='
    t_not_equal = '<>'
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
    t_logic_operation = r"(=|<=|>=|<|>)"
    t_add = "\+"
    t_substract = "-"
    t_multiply = "\*"
    t_divide = "/"
    t_open_parenthesis = "\("
    t_close_parenthesis = "\)"
    
    def t_ident(self, t):
        r"[a-z|A-Z]\w{0,10}"
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
        t.lexer.lineno += t.value.count('\n')
    
    def t_error(self, t):
        raise TypeError("Unknown text '%s' at %s" % (t.value, t.lexer.lineno))
    


    
