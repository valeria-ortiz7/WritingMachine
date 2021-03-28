import ply.lex as lex
from ply.lex import TOKEN

"""
Writing Machine

lexer.py: Imprime la línea que se recorre y los tokens en forma de pares ordenados 

Para correr el programa:
   1. En CMD "pip install ply" y luego "pip install pyhcl"
   2. Luego igual en CMD a la ubicación del archivo (cd Documentos o Descargas o c://Users/nombre...) y
   correr "python lexer.py"

TODO: Solucionar la detección de multiplicaciones

"""

# Lista de palabras reservadas, se hace aparte de los tokens para no generar una expresión regular para cada una
palabras_reservadas = {
    'Def'                       : 'DEF',
    'Put'                       : 'PUT',
    'Add'                     : 'ADD',
    'ContinueUp'       : 'CONTINUEUP',
    'ContinueDown'  : 'CONTINUEDOWN',
    'ContinueRight:'  : 'CONTINUERIGHT',
    'ContinueLeft'      : 'CONTINUELEFT',
    'Pos'                       : 'POS',
    'PosX'                     : 'POSX',
    'PosY'                     : 'POSY',
    'UseColor'             : 'USECOLOR',
    'Down'                   : 'DOWN',
    'Up'                        : 'UP',
    'Begin'                   : 'BEGIN',
    'Speed'                 : 'SPEED',
    'Run'                      : 'RUN',
    'Repeat'                : 'REPEAT',
    'If'                           : 'IF',
    'IfElse'                    : 'IFELSE',
    'Until'                     : 'UNTIL',
    'While'                   : 'WHILE',
    'Equal'                   : 'EQUAL',
    'And'                     : 'AND',
    'Or'                        : 'OR',
    'Greater'               : 'GREATER',
    'Smaller'               : 'SMALLER',
    'Substr'                 : 'SUBSTR',
    'Random'             : 'RANDOM',
    'Mult'                    : 'MULT',
    'Power'                 : 'POWER',
    'Div'                       : 'DIV',
    'Sum'                     : 'SUM',
    'MAIN'                  : 'MAIN',
    'PARA'                  :  'PARA',
    'FIN'                      : 'FIN'
    }


# Lista de tokens que identificará el programa
# Se agrega la lista de palabras reservadas al final
tokens = ['PARENTESISIZQ',
                  'PARENTESISDER',
                  'INT',
                  'PLUS',
                  'RESTA',
                  'DIVISION',
                  'MULTIPLICACION',
                   'POTENCIA',
                  'MAYORQUE',
                  'MENORQUE',
                  'PYC',
                  'COMA',
                  'IGUAL',
                  'IGUALES',
                  'CORCHETEIZQ',
                  'CORCHETEDER',
                  'STRING',
                  'ID',
                  'TRUE',
                  'FALSE'] + list(palabras_reservadas.values())


# Expresiones regulares de los tokens
t_ignore = '  \t\n' # Esto indica que ignorará tabs, espacios en blanco
t_ignore_COMENTARIO = r'--.*' # Ignorará los comentarios (empiezan con --)
t_IGUALES = r'=='
t_PLUS    = r'\+'
t_RESTA = r'-'
t_PARENTESISIZQ = r'\('
t_PARENTESISDER = r'\)'
t_DIVISION = r'/'
t_MULTIPLICACION = '\*'
t_POTENCIA = r'\^'
t_MAYORQUE = r'>'
t_MENORQUE = r'<'
t_PYC = r';'
t_COMA = r','
t_IGUAL = r'='
t_CORCHETEIZQ = r'\['
t_CORCHETEDER = r'\]'
t_STRING = r'"[a-zA-Z0-9_ ]*"'
""" REGLAS DEL LEXER """


# Identifica las variables del programa, excluye las palabras reservadas
def t_ID(token):
   # Define como se ve una variable o ID
   r'[a-zA-Z_][a-zA-Z_0-9@&]*'
   # Si es una palabra reservada, devuelve una tupla con la palabra y el valor
   if token.value in palabras_reservadas:
      # token.type devuelve los valores de arriba (p.e: token.type devuelve de t_CORCHETEDER : CORCHETEDER)
      token.type = palabras_reservadas[token.value]
   # Regresa la variable
   return token

# Define el token del valor booleano TRUE
def t_TRUE(token):
   r'(TRUE)'
   token.value = True
   return  token

# Define el token del valor booleano FALSE
def t_FALSE(token):
   r'(FALSE)'
   token.value = False
   return  token

# Regla de expresión regular para un número (int)
def t_INT(token):
   # Define un INT como un token de uno o más dígitos
   r'\d+'
   if token.value in palabras_reservadas:
      token.type = palabras_reservadas[token.value]
   # Convierte el valor de token a int y se lo asigna en su propiedad de "Valor"
   token.value = int(token.value)
   # Regresa el token con el valor del número en forma de int
   return token


# Se define el token "newline" para que el lexer pueda saber actualizar el número de línea que está recorriendo (útil en el futuro para indicar errores)
def t_newline(token):
   r'\n+'
   token.lexer.lineno += token.value.count("\n")
   return token
   

# Regla para manejar los errores
def t_error(token):
   # Si hay un caracter para el cual no existe un token (p.e: '?' o '!', imprime Caracter no permitido y el caracter al lado)
   print("Caracter no permitido '{0} en la linea {1}'".format(token.value[0], token.lineno))
   token.lexer.skip(1)
   

# Maneja el fin del archivo (EOF o End-Of-File)
def t_eof(t):
   return None


# Construir el lexer después de crear las reglas
lexer = lex.lex()

# Prueba para el lexer
   # Detecta e ignore comentarios - Check
   # Diferencia entre ID y String - Check
   # Detecta palabras reservadas - Check
   # Recibe _, & y @ como caracteres aceptados para un string - Check
   
lexer.input("""x_a = 3 * 4 - 5 * 6 + -2 ? ContinueUp
PARA
°
FIN""")


print("\n--------- Resultados del lexer: (Incluye errores que debe dar) ---------")
#Mientras hayan tokens, los imprime en el respectivo par ordenado
while True:
   token = lexer.token()

   # Si se acaban los tokens del input, se acaba
   if not token:
      break

   # Imprime la línea y, en forma de par ordenado, el tipo de token y qué fue lo que catalogó de esa manera
   print("En la linea " + str(token.lineno) + " se encontró el token: "
            + '(' + str(token.type) + ', ' + str(token.value) + ')')
   
