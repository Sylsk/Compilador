import ply.lex as lex

# Palabras reservadas
reserved = {
    'puede_ser_pa': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'print': 'PRINT'
}

# Definición de tokens
tokens = [
    'NUMBER', 'ID', 'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LESS', 'GREATER',
    'AND', 'OR', 'NOT', 'SEMICOLON', 'COMMA', 'STRING'  # Añadido 'COMMA'
] + list(reserved.values())

# Definición de los patrones regulares para cada token
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_EQUALS     = r'='
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_LESS       = r'<'
t_GREATER    = r'>'
t_AND        = r'&&'
t_OR         = r'\|\|'
t_NOT        = r'!'
t_SEMICOLON  = r';'
t_COMMA      = r','   # Definición del token 'COMMA'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Definición de expresiones regulares para tokens complejos
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Eliminar las comillas
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verificar si es una palabra reservada
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convertir a entero
    return t

# Manejar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejar errores léxicos
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()
