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
2. Generar las reglas para todo a partir de las reglas de POS

"""

# Lista de variables almacenadas. Guardará las variables creadas en el diccionario como {ID : valor}
variables = {}

variablesbool = {}
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
                 | pos
                 | condicion

   '''
   p[0] = p[1]


""" Asignaciones """

# Definición de asignación
def p_sentencia_asignacion(p):
   ''' sentencia : DEF ID IGUAL valor PYC
                 | DEF ID IGUAL TRUE PYC
                 | DEF ID IGUAL FALSE PYC
   '''
   p[0] = variables[p[2]] = p[4]
   if p[4] == "True" or p[4] == "False":
       variablesbool[p[2]] = p[4]

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
   ''' add : ADD CORCHETEIZQ ID CORCHETEDER PYC
           | ADD CORCHETEIZQ ID ID CORCHETEDER PYC
           | ADD CORCHETEIZQ ID INT CORCHETEDER PYC
   '''

   # Revisa primero si el ID existe en el diccionario, en caso de que no, da el error
   if p[3] not in variables:
         print("ERROR: No se puede incrementar en 1 al identificador indefinido {0} en la linea {1}\n".format(p[3], p.lineno(3)))

   # Si sí existe
   else:

      # Si solo recibe Add[id]
      if len(p) == 6:
         p[0] = variables[p[3]] = variables[p[3]] + 1

      # Si recibe Add[id var]
      elif len(p) == 7:
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
   # Si lo que le sigue es un número o expresión
   if isinstance(p[2], int):
      p[0] = p[2]

   # Si le sigue un ID
   if not isinstance(p[2], int):
      if p[2] in variables:
         p[0] = variables[p[2]]

      if p[2] not in variables:
         print("ERROR: No se puede mover n cantidades con el identificador indefinido {0}\n".format(p[2]))

""" Pos """

# Definicion de Pos
def p_pos(p):
    ''' pos : POS CORCHETEIZQ expresion COMA expresion CORCHETEDER PYC
            | POS CORCHETEIZQ valor COMA valor CORCHETEDER PYC
            | POS CORCHETEIZQ valor COMA expresion CORCHETEDER PYC
            | POS CORCHETEIZQ expresion COMA valor CORCHETEDER PYC
            | POSX expresion PYC
            | POSX valor PYC
            | POSY expresion PYC
            | POSY valor PYC
    '''
    # Si es Pos[]
    if len(p) == 8:
        if isinstance(p[3], int) and isinstance(p[5],int):
            p[0] = p[3] , p[5]
        else:
            if (p[3] in variables and p[5] in variables) or (isinstance(p[3], int) and p[5] in variables) or (p[3] in variables and isinstance(p[5], int)):

                if isinstance(p[3],int):
                    if (isinstance(variables[p[5]],int)):
                        p[0] = p[3] , variables[p[5]]
                    else:
                        print("ERROR: No se puede cambiar la posicion con el identificador booleano  {0}\n".format(p[5]))
                elif isinstance(p[5],int):
                    if isinstance(variables[p[3]], int):
                        p[0] = variables[p[3]] , p[5]
                    else:
                        print("ERROR: No se puede cambiar la posicion con el identificador booleano  {0}\n".format(p[3]))
                elif isinstance(variables[p[3]],int) and isinstance(variables[p[5]],int):
                    p[0] = variables[p[3]] , variables[p[5]]
                else:
                    if not isinstance(variables[p[5]],int):
                        print("ERROR: No se puede cambiar la posicion con el identificador booleano  {0}\n".format(p[5]))
                    elif not isinstance(variables[p[3]],int):
                        print("ERROR: No se puede cambiar la posicion con el identificador booleano  {0}\n".format(p[3]))

            elif (p[3] not in variables):
                print("ERROR: No se puede cambiar la posicion con el identificador indefinido  {0}\n".format(p[3]))
            elif (p[5] not in variables):
                print("ERROR: No se puede cambiar la posicion con el identificador indefinido  {0}\n".format(p[5]))
    # Si es PosX/PosY
    if len(p) == 4:
        if (isinstance(p[2], int)):
            p[0] = p[2]
        elif p[2] in variables:
            p[0] = variables[p[2]]
        elif p[2] not in variables:
                print("ERROR: No se puede cambiar la posicion con el identificador indefinido  {0}\n".format(p[3]))


""" Use Color"""

def p_usecolor(p):
    '''sentencia : USECOLOR valor PYC
                 | USECOLOR expresion PYC
    '''
    if isinstance(p[2],int):
        if 1<=p[2]<=3:
            p[0] = p[2]
        else:
            print("ERROR: Los valores aceptados para UseColor son 1,2,3 ")

    else:
        if p[2] in variablesbool:
            print("ERROR: No se puede cambiar el color con el identificador booleano  {0}\n".format(p[2]))
        elif (p[2] in variables):
            if 1 <= variables[p[2]] <= 3:
                p[0] = variables[p[2]]
            else:
                print("ERROR: Los valores aceptados para UseColor son 1,2,3 ")
        else:
            print("ERROR: No se puede cambiar la posicion con el identificador indefinido  {0}\n".format(p[2]))


""" Write """

def p_write(p):
    '''sentencia : DOWN PYC
                 | UP PYC
    '''
    p[0] = p[1]

""" Begin """

def p_begin(p):
    '''sentencia : BEGIN PYC
    '''
    p[0] = (1,1)

""" Speed """

def p_speed(p):
    '''sentencia : SPEED expresion PYC
                 | SPEED valor PYC
    '''
    if isinstance(p[2],int):
        p[0] = p[2]
    else:
        if p[2] in variablesbool:
            print("ERROR: No se puede cambiar la velocidad con el identificador booleano  {0}\n".format(p[2]))
        elif p[2] in variables:
            p[0] = variables[p[2]]
        else:
            print("ERROR: No se puede cambiar la velocidad con el identificador indefinido  {0}\n".format(p[2]))


""" Run/Repeat"""

def p_run(p):
    '''sentencia : RUN CORCHETEIZQ sentencias CORCHETEDER PYC
    '''
    p[0] = p[3]

def p_repeat(p):
    '''sentencia : REPEAT valor CORCHETEIZQ sentencias CORCHETEDER PYC
                 | REPEAT expresion CORCHETEIZQ sentencias CORCHETEDER PYC
    '''
    if isinstance(p[2],int):
        p[0] = [p[2]] + p[4]
    else:
        if p[2] in variablesbool:
            print("ERROR: No se puede recibir n como un identificador booleano  {0}\n".format(p[2]))
        elif p[2] in variables:
            p[0] = [variables[p[2]]] + p[4]
        else:
            print("ERROR: No se puede recibir n como un identificador indefinido  {0}\n".format(p[2]))

""" If """

def p_if(p):
    ''' sentencia : IF condicion CORCHETEIZQ sentencias CORCHETEDER PYC
    '''
    if p[2] == True:
        p[0] = p[4]

def p_ifelse(p):
    ''' sentencia : IFELSE condicion CORCHETEIZQ sentencias CORCHETEDER CORCHETEIZQ sentencias CORCHETEDER PYC
    '''
    if p[2] == True:
        p[0] = p[4]
    else:
        p[0] = p[7]

""" Iteracion """

def p_until(p):
    ''' sentencia : UNTIL CORCHETEIZQ sentencias CORCHETEDER CORCHETEIZQ condicion CORCHETEDER PYC
    '''
    cont = 1
    print("Until")
    while p[6] == True:
        cont = cont + 1
        print(p[6])
    p[0] = [cont] + p[3]


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

#Definicion de comparadores

def p_condiciones(p):
    '''condicion : expresion MAYORQUE expresion
                 | expresion MENORQUE expresion
                 | expresion IGUALES expresion
                 | expresion MAYORQUE valor
                 | expresion MENORQUE valor
                 | expresion IGUALES valor
                 | valor MAYORQUE valor
                 | valor MENORQUE valor
                 | valor IGUALES valor
                 | valor MAYORQUE expresion
                 | valor MENORQUE expresion
                 | valor IGUALES expresion
    '''
    print("xond")
    # Mayor

    if isinstance(p[1],int) and isinstance(p[3],int):
        if p[2] == '>':
            if p[1] > p[3]:
                p[0] = True
            else:
                p[0] = False
        elif p[2] == '<':
            if p[1] < p[3]:
                p[0] = True
            else:
                p[0] = False
        elif p[2] == '==':
            if p[1] == p[3]:
                p[0] = True
            else:
                p[0] = False
    else:
        if isinstance(p[1],int):
            if p[3] in variablesbool:
                print("ERROR: No se puede comparar el identificador booleano {0} ".format(p[3]) + "con un int")
            elif p[3] in variables:
                if p[2] == '>':
                    if p[1] > variables[p[3]]:
                        p[0] = True
                    else:
                        p[0] = False
                elif p[2] == '<':
                    if p[1] < variables[p[3]]:
                        p[0] = True
                    else:
                        p[0] = False
                elif p[2] == '==':
                    if p[1] == variables[p[3]]:
                        p[0] = True
                    else:
                        p[0] = False
            else:
                print("ERROR: No se puede comparar con el identificador indefinido {0}\n".format(p[3]))

        elif isinstance(p[3],int):
            if p[1] in variablesbool:
                print("ERROR: No se puede comparar el identificador booleano {0} ".format(p[1]) + "con un int")
            elif p[1] in variables:
                if p[2] == '>':
                    if variables[p[1]] > p[3]:
                        p[0] = True
                    else:
                        p[0] = False
                elif p[2] == '<':
                    if variables[p[1]] < p[3]:
                        p[0] = True
                    else:
                        p[0] = False
                elif p[2] == '==':
                    if variables[p[1]] == p[3]:
                        p[0] = True
                    else:
                        p[0] = False
            else:
                print("ERROR: No se puede comparar con el identificador indefinido {0}\n".format(p[1]))
        else:
            if p[2] == '>' or p[2] == '<':
                print("Error: las comparaciones de mayor o menor solo se pueden realizar con enteros")
            else:
                if p[1] in variablesbool:
                    if p[3] in variablesbool:
                        if variables[p[1]] == variables[p[3]]:
                            p[0] = True
                        else:
                            p[0] = False
                    elif p[3] == "True" or p[3] == "False":
                        if variables[p[1]] == p[3]:
                            p[0] = True
                        else:
                            p[0] = False
                elif p[3] in variablesbool:
                    if p[1] in variablesbool:
                        if variables[p[1]] == variables[p[3]]:
                            p[0] = True
                        else:
                            p[0] = False
                    elif p[1] == "True" or p[1] == "False":
                        if variables[p[3]] == p[1]:
                            p[0] = True
                        else:
                            p[0] = False
                elif (p[1] == "True" or p[1] == "False") and (p[3] == "True" or p[3] == "False"):
                    if p[1] == p[3]:
                        p[0] = True
                    else:
                        p[0] = False
                else:
                    print("Error: las comparaciones son validas solo para enteros o booleanos")




    # Iguales


""" ERRORES """

# Manejo de errores
def p_error(p):
   print(p)
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
print("\nResultados del parser:") # Nueva linea solo para separar los resultados del parser del lexer
print(yacc.parse("Def sds = 1; Def ass = jkjk;"))
print(yacc.parse(" Until [Add [sds];] [sds<3]; "))
print(yacc.parse("3+4+6-4"))
print(yacc.parse("(1+2)+2"))
print(yacc.parse("3 + (4 / 2)"))
print(yacc.parse("-3"))
print("\nDiccionario de variables almacenadas:\n", variables)
print("\nDiccionario de variables almacenadas:\n", variablesbool)
