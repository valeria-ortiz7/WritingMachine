# Importa el módulo yacc para el compilador
import ply.yacc as yacc

# Pretty Printer
import pprint

# Sys para leer argumentos
import sys

# Generación de números aleatorios
import random

# Para generacion de errores
numero_linea = 1

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

# Lista de errores del programa
lista_errores = []

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
                           | operacion
                           | condicion
                           | operadorlogico
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
      print("ERROR: No se puede cambiar el valor del identificador '{0}' indefinido en la linea {1}\n".format(p[2], p.lineno(1)))

# Add: Incrementa el valor de una variable
def p_add(p):
   ''' add : ADD CORCHETEIZQ ID CORCHETEDER
                 | ADD CORCHETEIZQ ID ID CORCHETEDER
                 | ADD CORCHETEIZQ ID INT CORCHETEDER
   '''

   # Revisa primero si el ID existe en el diccionario, en caso de que no, da el error
   if p[3] not in variables:
         print("ERROR: No se puede incrementar en 1 al identificador indefinido {0} en la linea {1}\n".format(p[3], p.lineno(1)))

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
            print("ERROR: No se puede incrementar a {0} en el identificador indefinido {1} en la linea {2}\n".format(p[3], p[4], p.lineno(1)))
            

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
   p.lineno(1)
   
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

  # Potencia
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


""" CONDICIONES """
def p_condicion(p):
   """ condicion : expresion MAYORQUE expresion
                            | expresion MENORQUE expresion
                            | expresion MENOROIGUAL expresion
                            | expresion MAYOROIGUAL expresion
                            | expresion IGUAL expresion
                            | valor IGUAL valor
                            | valor  MAYORQUE valor 
                            | valor  MENORQUE valor 
                            | valor  MENOROIGUAL valor 
                            | valor  MAYOROIGUAL valor 
   """
   # Variables temporales para la evaluación
   tempX = 0
   tempY = 0

   # Asigna los valores dependiendo si es ID o un int
   if p[1] and p[3] in variables:
      tempX = variables[p[1]]
      tempY = variables[p[3]]
   elif p[1] in variables and isinstance(p[3], int):
      tempX = variables[p[1]]
      tempY = p[3]
   elif p[3] in variables and isinstance(p[1], int):
      tempX = p[1]
      tempY = variables[p[3]]

   # Mayorque
   if p[2] == '>':
      p[0] = tempX >tempY

   # MayorOIgual
   elif p[2] == '>=':
      p[0] = tempX >= tempY

   # MenorQue
   elif p[2] == '<':
      p[0] = tempX < tempY

    # MenorOIgual
   elif p[2] == '<=':
      p[0] =  tempX <= tempY

    # Igual
   elif p[2] == '=':
      p[0] = tempX == tempY


""" COMPARADORES """

# Definición de Equal
def p_equal(p):
   """ condicion : EQUAL PARENTESISIZQ expresion COMA expresion PARENTESISDER PYC
   """

   # Si son iguales
   if p[3] == p[5]:
      p[0] = True

   # Si no son iguales
   else:
      p[0] = False

# Definición de Greater
def p_greater(p):
   """ condicion : GREATER PARENTESISIZQ expresion COMA expresion PARENTESISDER PYC
   """
   
   # Si N1 es mayor
   if p[3] > p[5]:
      p[0] = True
   else:
      p[0] = False


# Definición de Smaller
def p_smaller(p):
   """ condicion : SMALLER PARENTESISIZQ expresion COMA expresion PARENTESISDER PYC
   """
   
   # Si N1 es menor
   if p[3] < p[5]:
      p[0] = True
   else:
      p[0] = False

""" OPERADORES LÓGICOS """

# Definición de And
def p_and(p):
   """ operadorlogico : AND PARENTESISIZQ condicion COMA condicion PARENTESISDER PYC 
   """

   # Si son verdaderas
   if p[3] == True and p[5] == True:
      p[0] = True

   # Si no son verdaderas
   else:
      p[0] = False

# Definición de Or
def p_or(p):
   """ operadorlogico : OR PARENTESISIZQ condicion COMA condicion PARENTESISDER PYC 
   """

   # Si alguna es verdadera
   if p[3] == True or p[5] == True:
      p[0] = True

   # Si ninguna es verdadera
   else:
      p[0] = False


""" Operaciones """

# Definición de Substract N2 a N1
def p_substr(p):
   """ operacion : SUBSTR PARENTESISIZQ expresion COMA expresion PARENTESISDER PYC
   """
   p[0] = p[3] - p[5]


# Definición de Random(n)
def p_random(p):
   """ operacion : RANDOM PARENTESISIZQ expresion PARENTESISDER PYC
   """
   # Si el número es menor a 0 genera un número entre [n, 0]
   if p[3] < 0:
      p[0] = random.randint(p[3], 0)

   # Si el número es mayor a 0 genera un número entre [0, n]
   else:
      p[0] = random.randint(0, p[3])


# Definición de power
def p_power(p):
   """ operacion : POWER PARENTESISIZQ expresion COMA expresion PARENTESISDER PYC
   """
   p[0] = pow(p[3], p[5])

def p_power_error(p):
      'operacion : POWER error PYC'
      print("ERROR: Error de sintaxis en la expresión Power", p)


# Definición de Div
def p_div(p):
   """ operacion : DIV PARENTESISIZQ expresion COMA expresion PARENTESISDER PYC
   """
   p[0] = p[3] / p[5]


""" ERRORES """

# Manejo de errores
def p_error(p):
   if p is not None:
      print("Error de sintaxis en el token:", p.type, p.lineno)
      parser.errok()
   else:
      print("Entrada inesperada")
      
      
   # Look-ahead para buscar el ";" del final (AUN NO IMPLEMENTADO)
   while True:
      # Obtiene el siguiente token
      tok = parser.token()
      # Si no detecta punto y coma
      if not tok:
         break
   # Reinicia el parser
   parser.restart()

# Construye el parser
parser = yacc.yacc()

# Pruebas para el parser
print("\n--------- Resultados del parser: (Incluye errores que debe dar) ---------") # Nueva linea solo para separar los resultados del parser del lexer

# Crea el printer para poder imprimir tanto en el Shell de Python como en CMD
pp = pprint.PrettyPrinter(indent = 2)

# Implementación para leer un archivo que será el insumo del parser
with open(archivo_programa, 'r') as archivo:
   insumo = archivo.read()
   # Imprime el resultado
   pp.pprint(parser.parse(insumo))

# Imprime el diccionario de variables creadas/modificadas durante el programa
print("\nDiccionario de variables almacenadas:\n", variables)
