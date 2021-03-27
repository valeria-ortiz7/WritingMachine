# Importa el módulo yacc para el compilador
import ply.yacc as yacc

# Pretty Printer
import pprint

# Sys para leer argumentos
import sys

# Regresa el número de argumentos en la línea de comandos
numero_argumentos = len(sys.argv)

# Según la cantidad de argumentos, corre el programa
if numero_argumentos != 2:
   print("\n Uso: [archivo.py] [archivo.txt]")
   sys.exit(1)

# Si se reciben los dos parámetros, asigna el segundo como el archivo a leer
else:
   archivo_programa = sys.argv[1]


# Se importan los tokens creados en el otro archivo
from lexer import tokens

"""
Writing Machine

Parser: Genera el árbol de parseo. Imprime los resultados del parseo.

Para correr el programa:
   1. En CMD "pip install ply" y luego "pip install pyhcl" 
   2. Luego igual en CMD a la ubicación del archivo (cd Documentos o Descargas o c://Users/nombre...) y
   correr "python parser.py [nombre_archivo].txt" El archivo de lexer.py tiene que estar en la misma carpeta

TODO:
1. Generar los errores para cada error de sintaxis
2. Ignorar el punto y coma que va al final de cada expresión para evitar errores
3. Generar las reglas para todo

"""

# Lista de variables almacenadas. Guardará las variables creadas en el diccionario como {ID : valor}
variables = {}

# Lista de funciones almacenadas del programa
funciones = {}

# Precedencia para asignar a las operaciones
precedence = (
        ('left', 'PLUS', 'RESTA'),
        ('left', 'MULTIPLICACION', 'DIVISION'),
        ('right', 'UMENOS'),
        ('right', 'POTENCIA')
        )

# Se definen las reglas del parser, el nombre no importa siempre y cuando inicie con "p_"

""" Sentencias """

# Maneja varias sentencias en un programa
def p_sentencias(p):
   ''' sentencias : sentencias sentencia
                            | sentencia
   '''
   if len(p) == 2:
      p[0] = [p[1]]
   else:
      p[0] = p[1] + [p[2]]


# Definición de  sentencia
def p_sentencia_expr(p):
   ''' sentencia : expresion
                           | add
                           | continue
   '''
   p[0] = p[1]
        

""" Asignaciones """

# Definición de asignación
def p_sentencia_asignacion(p):
   ''' sentencia : DEF ID IGUAL valor PYC
   '''
   p[0] = variables[p[2]] = p[4]

# Le cambia el valor a una variable ya existente
def p_sentencia_cambio(p):
   ''' sentencia : PUT ID IGUAL valor PYC
                           | PUT ID IGUAL expresion PYC
   '''
   # Si la variable ya existe, le cambia el valor
   if p[2] in variables:
      p[0] = variables[p[2]] = p[4]

   # Si no existe, da error de variable indefinida
   else:
      print("ERROR: No se puede cambiar el valor del identificador '{0}' indefinido en la linea {1}\n".format(p[2], p.lineno(2)))

# Add: Incrementa el valor de una variable
def p_add(p):
   ''' add : ADD CORCHETEIZQ ID CORCHETEDER
                 | ADD CORCHETEIZQ ID ID CORCHETEDER
                 | ADD CORCHETEIZQ ID INT CORCHETEDER
   '''

   # Revisa primero si el ID existe en el diccionario, en caso de que no, da el error
   if p[3] not in variables:
         print("ERROR: No se puede incrementar en 1 al identificador indefinido {0} en la linea {1}\n".format(p[3], p.lineno(3)))

   # Si sí existe
   else:

      # Si solo recibe Add[id]
      if len(p) == 5:
         p[0] = variables[p[3]] = variables[p[3]] + 1

      # Si recibe Add[id var]
      elif len(p) == 6:
         if p[4] in variables:
            p[0] = variables[p[3]] = variables[p[3]] + variables[p[4]]

         if isinstance(p[4], int):
            p[0] = variables[p[3]] = variables[p[3]] + int(p[4])

         else:
            print("ERROR: No se puede incrementar a {0} en el identificador indefinido {1} en la linea {2}\n".format(p[3], p[4], p.lineno(3)))
            

# Definición de valor
def p_valor(p):
   ''' valor : INT
                  | ID
   '''
   p[0] = p[1]


""" ContinueX """

# Definición de Continue
def p_continue(p):
   ''' continue : CONTINUEUP INT PYC
                        | CONTINUEUP ID PYC
                        | CONTINUEUP expresion PYC
                        | CONTINUEDOWN INT PYC
                        | CONTINUEDOWN ID PYC
                        | CONTINUEDOWN expresion PYC
                        | CONTINUERIGHT INT PYC
                        | CONTINUERIGHT ID PYC
                        | CONTINUERIGHT expresion PYC
                        | CONTINUELEFT INT PYC
                        | CONTINUELEFT ID PYC
                        | CONTINUELEFT expresion PYC
   '''
   
   if isinstance(p[2], int):
      p[0] = p[2]

   if not isinstance(p[2], int):
      if p[2] in variables:
         p[0] = variables[p[2]]

      if p[2] not in variables:
         print("ERROR: No se puede mover n cantidades con el identificador indefinido {0}\n".format(p[2]))
   
   

""" Operaciones matemáticas básicas """

# Definicion de operación matemática
def p_expresion_op(p):
  '''expresion : expresion PLUS expresion
                         | expresion RESTA expresion
                         | expresion MULTIPLICACION expresion
                         | expresion DIVISION expresion
                         | expresion POTENCIA expresion
   '''

  # Suma
  if p[2] == '+': 
      p[0] = p[1] + p[3]
      
  # Resta
  elif p[2] == '-':
      p[0] = p[1] - p[3]

  # Multiplicación    
  elif p[2] == '*':
      p[0] = p[1] * p[3]

  # División
  elif p[2] == '/':
      p[0] = p[1] / p[3]

  elif p[2] == '^':
     p[0] = pow(p[1], p[3])


# Número negativo
def p_expresion_menos(p):
   '''expresion : RESTA expresion %prec UMENOS'''
   p[0] = -p[2]


# Define un término como parte de una expresión 
def p_expresion_num(p):
   'expresion : INT'
   p[0] = p[1]


# Expresiones entre paréntesis
def p_factor_expr(p):
   'expresion : PARENTESISIZQ expresion PARENTESISDER'
   p[0] = p[2]
   

""" ERRORES """

# Manejo de errores
def p_error(p):
   print("Error de sintaxis en el token:", p.type)
   parser.errok()

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
print("\n--------- Resultados del parser: (Incluye errores que debe dar) ---------") # Nueva linea solo para separar los resultados del parser del lexer

# Crea el printer para poder imprimir tanto en el Shell de Python como en CMD
pp = pprint.PrettyPrinter(indent = 4)

# Implementación para leer un archivo que será el insumo del parser
with open(archivo_programa, 'r') as archivo:
   insumo = archivo.read()
   # Imprime el resultado
   pp.pprint(parser.parse(insumo))

# Imprime el diccionario de variables creadas/modificadas durante el programa
print("\nDiccionario de variables almacenadas:\n", variables)
