from ply import lex
import sys

# Lista de tokens
tokens = ["number", 
          "equal",
          "not_equal",
          "comma",
          "semicolon",
          "assign",
          "logic_operation",
          "add",
          "substract",
          "multiply",
          "divide",
          "open_parenthesis",
          "close_parenthesis",
          "ident",
          "string",
          "program_end",
          "newline",
          ]
# http://stackoverflow.com/questions/5022129/ply-lex-parsing-problem
reserved = [ 'const', 'var', 'procedure', 'call', 'if', 'then', 'while', 'do', 'begin', 'end', 'odd', 'write', 'writeln', 'readln' ]
tokens += reserved

# Definicion de tokens
def t_number(t):
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
def t_ident(t):
    r"[a-z|A-Z]\w{0,10}"
    if t.value.lower() in reserved:
        t.type = t.value.lower()
    return t
t_ignore = r" \t"
t_writeln = "writeln" 
t_write = "write"
t_string = "'.*'"
t_program_end = "\."
def t_newline(t):
    r'[\n\r]+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    raise TypeError("Unknown text '%s' at %s" % (t.value,t.lexer.lineno))

lex.lex(debug=1)
lex.input(open(sys.argv[1],'r').read())


for tok in iter(lex.token, None):
    print tok.lineno,':',
    print repr(tok.type), repr(tok.value)
