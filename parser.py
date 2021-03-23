# Importa el módulo yacc para el compilador
import ply.yacc as yacc

# Se importan los tokens creados en el otro archivo
from lexer import tokens

"""
Writing Machine

Parser: Genera el árbol de parseo. Imprime los resultados del parseo.

Para correr el programa:
   1. En CMD "pip install ply" y luego "pip install pyhcl" 
   2. Luego igual en CMD a la ubicación del archivo (cd Documentos o Descargas o c://Users/nombre...) y
   correr "python parser.py" El archivo de lexer.py tiene que estar en la misma carpeta

TODO:
1. Generar los errores para cada error de sintaxis
2. Ignorar el punto y coma que va al final de cada expresión para evitar errores
3. Generar las reglas para todo

"""

# Se definen las reglas del parser, el nombre no importa siempre y cuando inicie con "p_"
# Cada palabra corresponde a un index por ejemplo en "expresion : expresion PLUS terminoino"
# expresion sería p[0], expresion p[1], PLUS p[2], termino p[3]

# Suma
def p_expresion_plus(p):
   'expresion : expresion PLUS termino'
   p[0] = p[1] + p[3]

# Resta o número negativo
def p_expresion_resta(p):
   '''expresion : expresion RESTA expresion
      | RESTA expresion'''
   
   # Si es una resta
   if (len(p) == 4):
      p[0] = p[1] - p[3]

   # Si solo hay tres términos, se define que no es una resta sino un -X
   elif (len(p) == 3):
      p[0] = p[2] * -1

# Define un término como parte de una expresión 
def p_expresion_termino(p):
   'expresion : termino'
   p[0] = p[1]

# Multiplicación
def p_termino_multiplicacion(p):
   'termino : termino MULTIPLICACION factor'
   p[0] = p[1] * p[3]

# División
def p_termino_div(p):
   'termino : termino DIVISION factor'
   p[0] = p[1] / p[3]

# Factor
def p_termino_factor(p):
   'termino : factor'
   p[0] = p[1]

# Números o int
def p_factor_num(p):
   'factor : INT'
   p[0] = p[1]

# Expresiones entre paréntesis
def p_factor_expr(p):
   'factor : PARENTESISIZQ expresion PARENTESISDER'
   p[0] = p[2]

""" ERRORES """

# Manejo de errores
def p_error(p):
   print("Error de sintaxis en el token:", p.type)

   # Look-ahead para buscar el ";" del final (AUN NO IMPLEMENTADO)
   while True:
      # Obtiene el siguiente token
      tok = parser.token()
      # Si no detecta punto y coma
      if not tok or tok.type == 'PYC':
         break
   # Reinicia el parser
   parser.restart()

   
# Construye el parser
parser = yacc.yacc()

# Pruebas para el parser
print("\nResultados del parser:") # Nueva linea solo para separar los resultados del parser del lexer
print(yacc.parse("2 - 3"))
print(yacc.parse("3*4"))
print(yacc.parse("3+4"))
print(yacc.parse("2 + 3/4"))
print(yacc.parse("3 + (4 / 2)"))
print(yacc.parse("-3"))
