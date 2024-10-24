import ply.yacc as yacc
from lexer import tokens

# Diccionario para almacenar variables en tiempo de ejecución
variables = {}

# Definir la precedencia de los operadores
precedence = (
    ('left', 'ELSE'),  # Para resolver el conflicto shift/reduce con 'else'
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'LESS', 'GREATER'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'NOT'),
)

# Clases para los nodos del AST
class Number:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class String:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class Variable:
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        return variables.get(self.name, 0)

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self):
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()
        
        if self.op == '+': return left_val + right_val
        if self.op == '-': return left_val - right_val
        if self.op == '*': return left_val * right_val
        if self.op == '/': return left_val / right_val
        if self.op == '<': return left_val < right_val
        if self.op == '>': return left_val > right_val
        if self.op == '&&': return left_val and right_val
        if self.op == '||': return left_val or right_val

class NotOp:
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self):
        return not self.expression.evaluate()

class Assign:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def execute(self):
        variables[self.name] = self.expression.evaluate()

class Print:
    def __init__(self, expressions):
        self.expressions = expressions  # Lista de expresiones

    def execute(self):
        evaluated_expressions = [expr.evaluate() for expr in self.expressions]
        print(*evaluated_expressions)

class IfElse:
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

    def execute(self):
        if self.condition.evaluate():
            self.if_block.execute()
        elif self.else_block:
            self.else_block.execute()

class WhileLoop:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def execute(self):
        while self.condition.evaluate():
            self.block.execute()

class ForLoop:
    def __init__(self, init_assign, condition, increment_assign, block):
        self.init_assign = init_assign
        self.condition = condition
        self.increment_assign = increment_assign
        self.block = block

    def execute(self):
        if self.init_assign:
            self.init_assign.execute()
        while True:
            if self.condition:
                if not self.condition.evaluate():
                    break
            self.block.execute()
            if self.increment_assign:
                self.increment_assign.execute()

class Block:
    def __init__(self, statements):
        self.statements = statements  # Lista de sentencias

    def execute(self):
        for stmt in self.statements:
            stmt.execute()

# Definir la regla inicial
def p_program(p):
    'program : statement_list'
    p[0] = Block(p[1])

# Definición de las listas de sentencias
def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

# Definición de las sentencias
def p_statement(p):
    '''statement : statement_print
                 | statement_assign
                 | statement_if
                 | statement_while
                 | statement_for
                 | block'''
    p[0] = p[1]

def p_statement_print(p):
    'statement_print : PRINT LPAREN expression_list RPAREN SEMICOLON'
    p[0] = Print(p[3])

def p_expression_list(p):
    '''expression_list : expression_list COMMA expression
                       | expression'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_statement_assign(p):
    'statement_assign : ID EQUALS expression SEMICOLON'
    p[0] = Assign(p[1], p[3])

def p_assign_expression(p):
    'assign_expression : ID EQUALS expression'
    p[0] = Assign(p[1], p[3])

def p_assign_expression_opt(p):
    '''assign_expression_opt : assign_expression
                             | empty'''
    p[0] = p[1]

def p_expression_opt(p):
    '''expression_opt : expression
                      | empty'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass  # p[0] es None

def p_statement_if(p):
    '''statement_if : IF LPAREN expression RPAREN statement
                    | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = IfElse(p[3], p[5])
    else:
        p[0] = IfElse(p[3], p[5], p[7])

def p_statement_while(p):
    'statement_while : WHILE LPAREN expression RPAREN statement'
    p[0] = WhileLoop(p[3], p[5])

def p_statement_for(p):
    'statement_for : FOR LPAREN assign_expression_opt SEMICOLON expression_opt SEMICOLON assign_expression_opt RPAREN statement'
    p[0] = ForLoop(p[3], p[5], p[7], p[9])

def p_block(p):
    'block : LBRACE statement_list RBRACE'
    p[0] = Block(p[2])

# Definición de expresiones
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression LESS expression
                  | expression GREATER expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = BinOp(p[1], p[2], p[3])

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = NotOp(p[2])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Number(p[1])

def p_expression_string(p):
    'expression : STRING'
    p[0] = String(p[1])

def p_expression_id(p):
    'expression : ID'
    p[0] = Variable(p[1])

def p_error(p):
    if p:
        print(f"Error de sintaxis en el token '{p.value}' (tipo {p.type}) en la línea {p.lineno}")
        parser.errok()
    else:
        print("Error de sintaxis: Fin inesperado del archivo.")

# Construcción del parser
parser = yacc.yacc(start='program')

# Función principal para ejecutar el código
def ejecutar_codigo(codigo):
    resultado = parser.parse(codigo)
    if resultado:
        resultado.execute()
