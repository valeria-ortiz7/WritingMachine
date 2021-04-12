# Importa el módulo yacc para el compilador
import ply.yacc as yacc

# Pretty Printer
import pprint

# Sys para leer argumentos
import sys

# Generación de números aleatorios
import random

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
import lexer
from lexer import tokens

"""
Writing Machine

Parser: Genera el árbol de parseo. Imprime los resultados del parseo.

Para correr el programa:
   1. En CMD "pip install ply" y luego "pip install pyhcl" 
   2. Luego igual en CMD a la ubicación del archivo (cd Documentos o Descargas o c://Users/nombre...) y
   correr "python parser.py [nombre_archivo].txt" El archivo de lexer.py tiene que estar en la misma carpeta

TODO:
1. Agregar los booleanos a lo que corresponda
2. Plantear cómo se va a definir el main
3. Detectar si no hay main
4. Hacer que el main sea el que guarde en variables y los procedimientos en variables_locales
5. Agregar Pos[], PosX, PosY, UseColor, Down, Up, Begin, Speed
6. Modificar la regla de "ordenes" para que acepte todas las funciones del programa (until, pos, procedimientos, etc)

"""
# Variables globales
global Iteracion
Iteracion = False


# Lista de variables almacenadas. Guardará las variables creadas en el diccionario como {ID : valor}
variables = {}

# Lista de variables locales almacenadas. Guardará las variables creadas en el diccionario como {ID : valor}
variables_locales = {}

# Lista de variables booleanas. Solo será para dar un seguimiento a el tipo de variable
variablesbool = {}

# Lista de funciones almacenadas del programa
funciones = {}

# Lista de errores del programa
lista_errores = []

# Cantidad de comentarios
comentarios = 0

# Main
main = 0

# Iteracion


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
                           | put
                           | continue
                           | pos
                           | operacion
                           | condicion
                           | operadorlogico
                           | comentario
                           | funcionreservada
                           | funcion
                           | funcioniter
   '''
   if isinstance(p[1],list):
       if p[1][0] == "Until":
           p[0] = until_exe(p[1])
       elif p[1][0] == "While":
           p[0] = while_exe(p[1])
       elif p[1][0] == "Repeat":
           p[0] = repeat_exe(p[1])
   else:
       p[0] = p[1]
        
def until_exe(until):
    recorrido = []
    if until[2][1] == "<":
        while value(until[2][0]) < value(until[2][2]):
            for i in exe(until[1]):
                recorrido.append(i)
    elif until[2][1] == "<=":
        while value(until[2][0]) <= value(until[2][2]):
            for i in exe(until[1]):
                recorrido.append(i)
    elif until[2][1] == ">":
        while value(until[2][0]) > value(until[2][2]):
            for i in exe(until[1]):
                recorrido.append(i)
    elif until[2][1] == ">=":
        while value(until[2][0]) >= value(until[2][2]):
            for i in exe(until[1]):
                recorrido.append(i)
    elif until[2][1] == "=":
        while value(until[2][0]) == value(until[2][2]):
            for i in exe(until[1]):
                recorrido.append(i)
    if recorrido == []:
        recorrido.append(exe(until[1]))

    return recorrido

def while_exe(while_):
    recorrido = []
    if while_[2][1] == "<":
        while value(while_[2][0]) < value(while_[2][2]):
            for i in exe(while_[1]):
                recorrido.append(i)
    elif while_[2][1] == "<=":
        while value(while_[2][0]) <= value(while_[2][2]):
            for i in exe(while_[1]):
                recorrido.append(i)
    elif while_[2][1] == ">":
        while value(while_[2][0]) > value(while_[2][2]):
            for i in exe(while_[1]):
                recorrido.append(i)
    elif while_[2][1] == ">=":
        while value(while_[2][0]) >= value(while_[2][2]):
            for i in exe(while_[1]):
                recorrido.append(i)
    elif while_[2][1] == "=":
        while value(while_[2][0]) == value(while_[2][2]):
            for i in exe(while_[1]):
                recorrido.append(i)
    if recorrido != []:
        return recorrido

def repeat_exe(repeat):
    recorrido = []
    cont = 0
    while cont < repeat[2]:
        for i in exe(repeat[1]):
            recorrido.append(i)
        cont = cont + 1
        
    return recorrido

def if_exe(if_):
    recorrido = []
    if if_[1][1] == "<":
        if value(if_[1][0])  < value(if_[1][2]):
            for i in exe(if_[2]):
                recorrido.append(i)
    elif if_[1][1] == "<=":
        if value(if_[1][0])  <= value(if_[1][2]):
            for i in exe(if_[2]):
                recorrido.append(i)
    elif if_[1][1] == ">":
        if value(if_[1][0])  > value(if_[1][2]):
            for i in exe(if_[2]):
                recorrido.append(i)
    elif if_[1][1] == ">=":
        if value(if_[1][0])  >= value(if_[1][2]):
            for i in exe(if_[2]):
                recorrido.append(i)
    elif if_[1][1] == "=":
        if value(if_[1][0])  == value(if_[1][2]):
            for i in exe(if_[2]):
                recorrido.append(i)
    if recorrido != []:
        return recorrido



def ifelse_exe(ifelse):
    recorrido = []
    if ifelse[1][1] == "<":
        if value(ifelse[1][0]) < value(ifelse[1][2]):
            for i in exe(ifelse[2]):
                recorrido.append(i)
        else:
            for i in exe(ifelse[3]):
                recorrido.append(i)
    elif ifelse[1][1] == "<=":
        if value(ifelse[1][0]) <= value(ifelse[1][2]):
            for i in exe(ifelse[2]):
                recorrido.append(i)
        else:
            for i in exe(ifelse[3]):
                recorrido.append(i)
    elif ifelse[1][1] == ">=":
        if value(ifelse[1][0]) >= value(ifelse[1][2]):
            for i in exe(ifelse[2]):
                recorrido.append(i)
        else:
            for i in exe(ifelse[3]):
                recorrido.append(i)
    elif ifelse[1][1] == ">":
        if value(ifelse[1][0]) > value(ifelse[1][2]):
            for i in exe(ifelse[2]):
                recorrido.append(i)
        else:
            for i in exe(ifelse[3]):
                recorrido.append(i)
    elif ifelse[1][1] == "=":
        if value(ifelse[1][0]) == value(ifelse[1][2]):
            for i in exe(ifelse[2]):
                recorrido.append(i)
        else:
            for i in exe(ifelse[3]):
                recorrido.append(i)
    return recorrido

def exe(listtoexe):
    recorrido = []
    for i in listtoexe:
        if isinstance(i, list):
            if i[0] == "Add":
                variables[i[1]] = variables[i[1]] + i[2]
            elif i[0] == "Put":
                variables[i[1]] = i[2]
            elif i[0] == "If":
                recorrido.append(if_exe(i))
            elif i[0] == "IfElse":
                recorrido.append(ifelse_exe(i))
            elif i[0] == "Until":
                recorrido.append(until_exe(i))
            elif i[0] == "While":
                recorrido.append(while_exe(i))
            elif i[0] == "Repeat":
                recorrido.append(repeat_exe(i))
            else:
                recorrido.append(i)
        else:
            recorrido.append(i)
    return recorrido

def value(x):
    if x in variables:
        return variables[x]
    else:
        return x

""" Asignaciones """

# Definición de asignación
def p_asignacion_global(p):
   ''' sentencia : DEF ID IGUAL valor PYC
                 | DEF ID IGUAL TRUE PYC
                 | DEF ID IGUAL FALSE PYC
   '''
   p[0] = variables[p[2]] = p[4]
   if p[4] == "True" or p[4] == "False":
       variablesbool[p[2]] = p[4]

# PUT: Le cambia el valor a una variable ya existente
def p_sentencia_cambio(p):
   ''' put : PUT ID IGUAL valor PYC
           | PUT ID IGUAL expresion PYC
   '''
   # Si la variable ya existe, le cambia el valor
   if p[2] in variables:
       p[0] = [p[1], p[2], value(p[4])]

   # Si no existe, da error de variable indefinida
   else:
      lista_errores.append("ERROR: No se puede cambiar el valor del identificador '{0}' indefinido en la linea {1}".format(p[2], p.lineno(2)))


# Add: Incrementa el valor de una variable
def p_add(p):
   ''' add : ADD CORCHETEIZQ ID CORCHETEDER PYC
           | ADD CORCHETEIZQ ID ID CORCHETEDER PYC
           | ADD CORCHETEIZQ ID INT CORCHETEDER PYC
   '''
   # Revisa primero si el ID existe en el diccionario, en caso de que no, da el error
   if p[3] not in variables:
         lista_errores.append("ERROR: No se puede incrementar en 1 al identificador indefinido {0} en la linea {1}".format(p[3], p.lineno(3)))

   # Revisa que el identificador sea de tipo entero
   elif p[3] in variablesbool:
         lista_errores.append("ERROR: No se puede incrementar en 1 al identificador booleano {0} en la linea {1}".format(p[3], p.lineno(3)))


   # Si sí existe
   else:

      # Si solo recibe Add[id]
      if len(p) == 6:
         p[0] = [p[1] , p[3] , 1]

      # Si recibe Add[id var]
      elif len(p) == 7:
         if p[4] in variablesbool:
            lista_errores.append("ERROR: No se puede incrementar con un valor booleano en la linea {1}".format(p[4], p.lineno(4)))

         elif p[4] in variables:
            p[0] = [p[1] , p[3] , variables[p[4]] ]

         elif isinstance(p[4], int):
            p[0] =  [p[1] , p[3] ,  int(p[4])]

         else:
            lista_errores.append("ERROR: No se puede incrementar a {0} en el identificador indefinido {1} en la linea {2}".format(p[3], p[4], p.lineno(4)))
            

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
      p[0] = [p[1], p[2]]

   if not isinstance(p[2], int):
      if p[2] in variablesbool:
         lista_errores.append("ERROR: No se puede mover n cantidades con el identificador booleano {0} en la linea {1}".format(p[2], p.lineno(2)))

      elif p[2] in variables:
         p[0] = [p[1], variables[p[2]]]

      elif p[2] not in variables:
         lista_errores.append("ERROR: No se puede mover n cantidades con el identificador indefinido {0} en la linea {1}".format(p[2], p.lineno(2)))






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
            p[0] = [p[1] , p[3] , p[5]]
        else:
            if (p[3] in variables and p[5] in variables) or (isinstance(p[3], int) and p[5] in variables) or (p[3] in variables and isinstance(p[5], int)):

                if isinstance(p[3],int):
                    if (isinstance(variables[p[5]],int)):
                        p[0] = [p[1], p[3] , variables[p[5]]]
                    else:
                        lista_errores.append("ERROR: No se puede cambiar la posicion con el identificador booleano  {0}\n".format(p[5]))
                elif isinstance(p[5],int):
                    if isinstance(variables[p[3]], int):
                        p[0] = [p[1] , variables[p[3]] , p[5]]
                    else:
                        lista_errores.append("ERROR: No se puede cambiar la posicion con el identificador booleano  {0}\n".format(p[3]))
                elif isinstance(variables[p[3]],int) and isinstance(variables[p[5]],int):
                    p[0] = [p[1] , variables[p[3]] , variables[p[5]]]
                else:
                    if not isinstance(variables[p[5]],int):
                        lista_errores.append("ERROR: No se puede cambiar la posicion con el identificador booleano  {0}\n".format(p[5]))
                    elif not isinstance(variables[p[3]],int):
                        lista_errores.append("ERROR: No se puede cambiar la posicion con el identificador booleano  {0}\n".format(p[3]))

            elif (p[3] not in variables):
                lista_errores.append("ERROR: No se puede cambiar la posicion con el identificador indefinido  {0}\n".format(p[3]))
            elif (p[5] not in variables):
                lista_errores.append("ERROR: No se puede cambiar la posicion con el identificador indefinido  {0}\n".format(p[5]))
    # Si es PosX/PosY
    if len(p) == 4:
        if (isinstance(p[2], int)):
            p[0] = [p[1] , p[2]]
        elif p[2] in variables:
            p[0] = [p[1] , variables[p[2]]]
        elif p[2] in variablesbool:
            lista_errores.append("ERROR: No se puede cambiar la posicion con el identificador indefinido  {0}\n".format(p[3]))
        elif p[2] not in variables:
            lista_errores.append("ERROR: No se puede cambiar la posicion con el identificador booleano  {0}\n".format(p[3]))


""" Use Color"""

def p_usecolor(p):
    '''sentencia : USECOLOR valor PYC
                 | USECOLOR expresion PYC
    '''
    if isinstance(p[2],int):
        if 1<=p[2]<=3:
            p[0] = p[2]
        else:
            lista_errores.append("ERROR: Los valores aceptados para UseColor son 1,2,3 ")

    else:
        if p[2] in variablesbool:
            print("ERROR: No se puede cambiar el color con el identificador booleano  {0}\n".format(p[2]))
        elif (p[2] in variables):
            if 1 <= variables[p[2]] <= 3:
                p[0] = variables[p[2]]
            else:
                lista_errores.append("ERROR: Los valores aceptados para UseColor son 1,2,3 ")
        else:
            lista_errores.append("ERROR: No se puede cambiar la posicion con el identificador indefinido  {0}\n".format(p[2]))


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
    p[0] = p[1]

""" Speed """

def p_speed(p):
    '''sentencia : SPEED expresion PYC
                 | SPEED valor PYC
    '''
    if isinstance(p[2],int):
        p[0] = [p[1] , p[2]]
    else:
        if p[2] in variablesbool:
            lista_errores.append("ERROR: No se puede cambiar la velocidad con el identificador booleano  {0}\n".format(p[2]))
        elif p[2] in variables:
            p[0] = [p[1] , variables[p[2]]]
        else:
            lista_errores.append("ERROR: No se puede cambiar la velocidad con el identificador indefinido  {0}\n".format(p[2]))



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


# Definición de comentarios
def p_comentario(p):
   'comentario : COMENTARIO'
   global comentarios
   comentarios = comentarios + 1
   p[0] = None


# Definicion de booleano
def p_bool(p):
   """ bool : TRUE
            | FALSE
   """
   p[0] = p[1]

""" CONDICIONES """

# Condicion
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
                 | bool IGUAL bool
                 | valor IGUAL bool
                 | bool IGUAL valor
   """
   # Variables temporales para la evaluación
   tempX = 0
   tempY = 0

   # Asigna los valores dependiendo si es ID o un int
   if (p[1] in variablesbool or p[1] == "True" or p[1] == "False") and (p[3] in variablesbool or p[3] == "True" or p[3] == "False"):
      if p[2] == "=":
         if p[3] in variablesbool and p[1] in variablesbool:
            tempX = variables[p[1]]
            tempY = variables[p[3]]
         elif p[1] in variablesbool:
            tempX = variables[p[1]]
            tempY = p[3]
         elif p[3] in variablesbool:
            tempX = p[1]
            tempY = variables[p[3]]
         else:
            tempX = p[1]
            tempY = p[3]
      else:
         lista_errores.append("ERROR: No se pueden realizar compraciones mayor o menor con entradas booleanas em la linea {1}".format(p[1], p.lineno(1)))


   elif p[1] in variables and p[3] in variables:
      tempX = variables[p[1]]
      tempY = variables[p[3]]
   elif p[1] in variables and isinstance(p[3], int):
      tempX = variables[p[1]]
      tempY = p[3]
   elif p[3] in variables and isinstance(p[1], int):
      tempX = p[1]
      tempY = variables[p[3]]
   else:
      tempX = p[1]
      tempY = p[3]

   # Mayorque
   if p[2] == '>':
      p[0] = (tempX >tempY)

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
                 | EQUAL PARENTESISIZQ valor COMA expresion PARENTESISDER PYC
                 | EQUAL PARENTESISIZQ expresion COMA valor PARENTESISDER PYC
                 | EQUAL PARENTESISIZQ valor COMA valor PARENTESISDER PYC
                 | EQUAL PARENTESISIZQ bool COMA valor PARENTESISDER PYC
                 | EQUAL PARENTESISIZQ valor COMA bool PARENTESISDER PYC
                 | EQUAL PARENTESISIZQ bool COMA bool PARENTESISDER PYC
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

# Definición de Subract N2 a N1
def p_substr(p):
   """ operacion : SUBSTR PARENTESISIZQ parametros PARENTESISDER PYC
   """
   resultado = p[3][0] * 2
   for i in p[3]:
      resultado = resultado - i
   p[0] = resultado


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


# Definición de Sum
def p_sum(p):
   """ operacion : SUM PARENTESISIZQ parametros PARENTESISDER PYC
   """
   
   # Como se recibe una lista de parámetros, se suman los parámetros recibidos
   resultado = 0
   for i in p[3]:
      resultado = resultado + i
      
   p[0] = resultado


# Definición de Mult
def p_mult(p):
   """ operacion : MULT PARENTESISIZQ parametros PARENTESISDER PYC
   """
   # Como se recibe una lista de parámetros, se multiplican los parámetros recibidos
   resultado = 1
   for i in p[3]:
      resultado = resultado * i

   p[0] = resultado


""" PARAMETROS DE OPERACIONES """


# Parametros (se dan en forma de una lista)
def p_parametros(p):
    '''parametros : expresion
                  | parametros COMA expresion
                  | valor
                  | parametros COMA valor
    '''

    # Si es solo una expresion
    if len(p) == 2:
       p[0] = [p[1]]

    # Si son más de dos
    else:
       p[0] = p[1] + [p[3]]


""" Funciones reservadas """


# Definición de run
def p_run(p):
   """ funcionreservada : RUN CORCHETEIZQ ordenes CORCHETEDER PYC
   """
   # Solo devuelve las órdenes a ejecutar
   p[0] = p[3]


# Definición de Repeat
def p_repeat(p):
   """ funcioniter : REPEAT valor CORCHETEIZQ ordenesiter CORCHETEDER PYC
   """
   times = 0

   if p[2] in variablesbool:
         lista_errores.append("ERROR: No se puede repetir n veces con una entrada booleana {0} en la linea {1}".format(p[2], p.lineno(1)))

   elif p[2] in variables:
   # Devuelve las ordenes a ejecutar repetidas N veces
      p[0] = [p[1] , p[4] , variables[p[2]]]
   else:
   # Devuelve las ordenes a ejecutar repetidas N veces
      p[0] = [p[1] , p[4] , p[2]]


# Definición de if
def p_if(p):
   """ funcionreservada : IF PARENTESISIZQ condicion PARENTESISDER CORCHETEIZQ ordenes CORCHETEDER PYC
   """
   # Si se cumple la condición, devuelve las ordenes a ejecutar
   p[0] = [p[1] , p[3] , p[6]]

# Definición de ifelse
def p_ifelse(p):

   """ funcionreservada : IFELSE PARENTESISIZQ condicion PARENTESISDER CORCHETEIZQ ordenes CORCHETEDER CORCHETEIZQ ordenes CORCHETEDER PYC
   """
   # Si se cumple la condición, devuelve las ordenes a ejecutar

   p[0] = [p[1] , p[3] , p[6], p[9]]


def p_if_iter(p):
    """ if : IF PARENTESISIZQ condicionciclo PARENTESISDER CORCHETEIZQ ordenesiter CORCHETEDER PYC
    """
    # Si se cumple la condición, devuelve las ordenes a ejecutar
    p[0] = [p[1], p[3], p[6]]


# Definición de ifelse
def p_ifelse_iter(p):
    """ ifelse : IFELSE PARENTESISIZQ condicionciclo PARENTESISDER CORCHETEIZQ ordenesiter CORCHETEDER CORCHETEIZQ ordenesiter CORCHETEDER PYC
    """
    # Si se cumple la condición, devuelve las ordenes a ejecutar

    p[0] = [p[1], p[3], p[6], p[9]]


# Definición de until
def p_until(p):
   """ funcioniter : UNTIL CORCHETEIZQ ordenesiter CORCHETEDER CORCHETEIZQ condicionciclo CORCHETEDER PYC
                        | UNTIL CORCHETEIZQ ordenesiter CORCHETEDER PARENTESISIZQ condicionciclo  PARENTESISDER PYC
   """
   # Devuelve el par ordenado con la respectiva condicion

   p[0] = [p[1],p[3],p[6]]



# Definición de while
def p_while(p):
   """ funcioniter : WHILE  CORCHETEIZQ condicionciclo CORCHETEDER CORCHETEIZQ ordenesiter CORCHETEDER PYC
                   | WHILE PARENTESISIZQ condicionciclo PARENTESISDER CORCHETEIZQ ordenesiter CORCHETEDER PYC
   """
   # Devuelve el par ordenado con la respectiva condicion
   p[0] = [p[1], p[6], p[3]]


def actualizar(p):
    print(p)

# Condición que debe ser devuelta para evaluar en los ciclos UNTIL y WHILE
def p_condicionciclo(p):
   """ condicionciclo : expresion MAYORQUE expresion
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
   # Crea la formación en forma de lista
   condicion = []
   for i in p:
      condicion.append(i)
   condicion.pop(0)

   # Devuelve la condición en forma de lista para evaluarla más fácil
   p[0] = condicion


""" ORDENES """

# Ordenes (se dan en forma de una lista de listas)
def p_ordenes(p):
    '''ordenes : continue
               | ordenes continue
               | add
               | ordenes add
               | ordenes funcionreservada
               | funcionreservada
               | ordenes funcioniter
               | funcioniter
    '''

    print(p[1])
    if len(p) == 2:
       p[0] = [p[1]]
    else:
       p[0] = p[1] + [p[2]]


def p_ordenes_iter(p):
    '''ordenesiter : continue
                   | ordenesiter continue
                   | add
                   | ordenesiter add
                   | ordenesiter ifelse
                   | ifelse
                   | ordenesiter if
                   | if
                   | ordenesiter operacion
                   | operacion
                   | ordenesiter put
                   | put
                   | ordenesiter funcioniter
                   | funcioniter
    '''
    if len(p) == 2:
       p[0] = [p[1]]
    else:
       p[0] = p[1] + [p[2]]


""" PROCEDIMIENTOS """

# Definición de procedimientos
def p_funciones(p):
   """ funcion : PARA ID CORCHETEIZQ parametros CORCHETEDER ordenes FIN
   """
      
   if p[2] in variables:
      lista_errores.append("ERROR: No se puede crear el procedimiento en la linea {0} con el nombre de una variable ya asignada".format(p.lineno(2)))

   if p[2] in funciones:
      lista_errores.append("ERROR: No se puede crear el procedimiento en la linea {0} con el nombre de un procedimiento ya creado".format(p.lineno(2)))
      
   else:
      p[0] = funciones[p[2]] = ['FUNCION', p[2], p[4], p[6]]   


""" ERRORES """

# Manejo de errores
def p_error(p):
   print("Error de sintaxis encontrado:")
   if p is not None:
      print("Error de sintaxis en el token {0} {1} en la línea {2}\n".format(p.type, p.value, p.lineno))
      parser.errok()
   else:
      print("Entrada inesperada\n")
      
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
pp = pprint.PrettyPrinter()

# Implementación para leer un archivo que será el insumo del parser
with open(archivo_programa, 'r') as archivo:
   insumo = archivo.read()

   resultado = parser.parse(insumo)

   # Verifica si hay al menos un comentario   
   if comentarios == 0:
      print("ERROR: El programa debe tener al menos un comentario")
      sys.exit(1)

   # Verifica si hay al menos una variable 
   if len(variables) == 0:
      print("ERROR: El programa debe tener al menos una asignación de variable")
      sys.exit(1)

   # Si no hay errores de sintaxis
   if resultado != None:
      # Imprime los errores del programa
      for error in lista_errores:
         print(error)
         
      print('\n') 
      pp.pprint(resultado)

with open("error.txt", "w+") as archivo_resultado:
   for i in lista_errores:
      archivo_resultado.write(i + '\n')
