# Importa el módulo yacc para el compilador
import ply.yacc as yacc

# Pretty Printer
import pprint

# Sys para leer argumentos
import sys

# Generación de números aleatorios
import random

# Define el archivo del programa
archivo_programa = "entrada.txt"

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
2. Agregar Pos[], PosX, PosY, UseColor, Down, Up, Begin, Speed
3. Modificar la regla de "ordenes" para que acepte todas las funciones del programa (until, pos, procedimientos, etc)
4. Verificar algunos errores
5. Agregar el resto de evaluaciones

"""

# Lista de variables almacenadas. Guardará las variables creadas en el diccionario como {ID : valor}
variables = {}

# Lista de variables globales almacenadas. Guardará las variables creadas en el diccionario como {ID : valor}
variables_globales = {}

# Lista de funciones almacenadas del programa
funciones = {} 

# Lista de errores del programa
lista_errores = []

# Cantidad de comentarios
comentarios = []

# Instrucciones para el Arduino
instrucciones = []

# Código que se va a ejecutar
codigo_main = []

# Verificaciones
main = 0
num_variables = 0
num_comentarios = 0

# Precedencia para asignar a las operaciones
precedence = (
        ('left', 'PLUS', 'RESTA'),
        ('left', 'MULTIPLICACION', 'DIVISION'),
        ('right', 'UMENOS'),
        ('right', 'POTENCIA')
        )

# Se definen las reglas del parser, el nombre no importa siempre y cuando inicie con "p_"


#################### SENTENCIAS ####################

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
                           | comentario
                           | funcionreservada
                           | funcion
                        
   '''
   p[0] = p[1]
        

#################### SENTENCIAS ####################

# Definición de asignación
def p_asignacion_global(p):
   ''' sentencia : DEF ID IGUAL valor PYC
   '''
   #Verifica que la asignación de la variable cumpla con el tamaño
   if len(p[2]) >= 3 and len(p[2])<= 10:
      global num_variables
      num_variables = num_variables + 1

      # Regresa la lista con la variable creada y su valor
      p[0] = ['DEF', p[2], p[4]]

   # Si no cumple con el tamaño
   else:
      lista_errores.append("ERROR: La variable {0} no se pudo definir ya que debe tener más de 3 posiciones y menos de 10 posiciones".format(p[2]))


# PUT: Le cambia el valor a una variable ya existente
def p_sentencia_cambio(p):
   ''' sentencia : PUT ID IGUAL valor PYC
                           | PUT ID IGUAL expresion PYC
   '''
   # Revisa si existe y si existe le asigna el valor
   variable = revisar_variable(p[2])

   # Si existe
   if variable is not False:
      p[0] = [p[1], p[2], p[4]]

   # Si no existe, da error de variable indefinida
   else:
      lista_errores.append("ERROR: No se puede cambiar el valor del identificador '{0}' indefinido en la linea {1}".format(p[2], p.lineno(2)))


#################### SENTENCIAS ####################

# Add: Incrementa el valor de una variable
def p_add(p):
   ''' add : ADD CORCHETEIZQ ID CORCHETEDER PYC
                 | ADD CORCHETEIZQ ID ID CORCHETEDER PYC
                 | ADD CORCHETEIZQ ID INT CORCHETEDER PYC
   '''
   # Toma el valor del identificador recibido independientemente del tamaño
   variable = revisar_variable(p[3]) 

   # Si solo se evalúa el primer identificador y el identificador existe
   if len(p) == 6 and variable is not False:
      p[0] = [p[1], p[3], variable + 1]

   # Si se evalúan dos identificadores y el primero existe
   elif len(p) == 7:
      # Revisa si existe la variable 2
      variable2 = revisar_variable(p[4])

      # Si existe, devuelve el add
      if variable2 is not False:
         p[0] = [p[1], p[3], p[4], variable + variable2]

      # Si no existe la variable 2 pero si la 1
      if variable2 is False:
         lista_errores.append("ERROR: No se incrementar el valor del identificador '{0}' indefinido en la linea {1}".format(p[4], p.lineno(4)))

      # Si no existe la variable 2 pero si la 1
      if variable is False:
         lista_errores.append("ERROR: No se incrementar el valor del identificador '{0}' indefinido en la linea {1}".format(p[3], p.lineno(3)))

   # Si no existe la variable 1
   else:
      lista_errores.append("ERROR: No se incrementar el valor del identificador '{0}' indefinido en la linea {1}".format(p[3], p.lineno(3)))
      

# Definición de valor
def p_valor(p):
   ''' valor : INT
                  | ID
   '''
   p[0] = p[1]


#################### FUNCIONES DE DIBUJO ####################

# Definición de Continue
def p_continue(p):
   ''' continue : CONTINUEUP valor PYC
                        | CONTINUEUP expresion PYC
                        | CONTINUEDOWN valor PYC
                        | CONTINUEDOWN expresion PYC
                        | CONTINUERIGHT valor PYC
                        | CONTINUERIGHT expresion PYC
                        | CONTINUELEFT valor PYC
                        | CONTINUELEFT expresion PYC
   '''
   # Si es un número
   if isinstance(p[2], int):
      p[0] = [p[1], p[2]]

   # Si es una variable
   if not isinstance(p[2], int):
      variable = revisar_variable(p[2])

      # Si la variable existe
      if variable is not False:
         p[0] = [p[1], variable]

      # Si la variable no existe
      else:
         lista_errores.append("ERROR: No se puede mover n cantidades con el identificador indefinido {0} en la linea".format(p[2], p.lineno(2)))
   

#################### Operaciones matemáticas básicas ####################

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
   '''expresion : INT
   '''
   p[0] = p[1]


# Expresiones entre paréntesis
def p_factor_expr(p):
   'expresion : PARENTESISIZQ expresion PARENTESISDER'
   p[0] = p[2]


#################### COMENTARIOS ####################

# Definición de comentarios
def p_comentario(p):
   'comentario : COMENTARIO'

   # Le suma al número de comentarios
   global num_comentarios
   num_comentarios = num_comentarios + 1

   # Agrega el comentario para luego verificar que haya uno en la primera línea
   comentarios.append(p[1])

   # Devuelve el comentario
   p[0] = p[1]


#################### CONDICIONES ####################

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
   """
   # Variables temporales para la evaluación
   tempX = 0
   tempY = 0

   # Si son variables, las asigna
   variable1 = revisar_variable(p[1])
   variable2 = revisar_variable(p[3])

   # Error
   error = False

   # Asigna los valores dependiendo si es ID o un int
   if variable1 is not False and variable2 is not False:
      tempX = variable1
      tempY = variable2

   # Revisa si la primera entrada es una variable y la segunda número
   elif variable1 is not False and isinstance(p[3], int):
      tempX = variable1
      tempY = p[3]

   # Revisa si la primera entrada es un número y la segunda variable
   elif variable2 is not False and isinstance(p[1], int):
      tempX = p[1]
      tempY = variable2

   # Revisa si la primera entrada es un número y la segunda número
   elif isinstance(p[1], int) and isinstance(p[3], int):
      tempX = p[1]
      tempY = p[3]

   # Si no es número y no existe
   elif not isinstance(p[1], int) and variable1 is False:
      lista_errores.append("ERROR: No se puede comparar con el identificador indefinido {0} en la línea {1}".format(p[1], p.lineno(1)))

   # Si no es número y no existe
   elif not isinstance(p[3], int) and variable2 is False:
      lista_errores.append("ERROR: No se puede comparar con el identificador indefinido {0} en la línea {1}".format(p[3], p.lineno(3)))
   
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


#################### COMPARADORES ####################

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


#################### OPERADORES LÓGICOS ####################

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


#################### OPERACIONES ####################

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


#################### PARAMETROS ####################


# Parametros (se dan en forma de una lista)
def p_parametros(p):
    '''parametros : expresion
                             | valor
                             | parametros COMA expresion
                             | parametros COMA valor'''

    # Si es solo una expresion
    if len(p) == 2:
       p[0] = [p[1]]

    # Si son más de dos
    else:
       p[0] = p[1] + [p[3]]


#################### FUNCIONES INTERNAS ####################


# Definición de run
def p_run(p):
   """ funcionreservada : RUN CORCHETEIZQ ordenes CORCHETEDER PYC
   """
   # Solo devuelve las órdenes a ejecutar
   p[0] = p[3]


# Definición de Repeat
def p_repeat(p):
   """ funcionreservada : REPEAT valor CORCHETEIZQ ordenes CORCHETEDER PYC
   """
   # Devuelve las ordenes a ejecutar repetidas N veces
   p[0] = p[2] * p[4]


#################### EVALUACIONES #################### 

# Definición de if
def p_if(p):
   """ funcionreservada : IF PARENTESISIZQ condicion PARENTESISDER CORCHETEIZQ ordenes CORCHETEDER PYC
   """
   # Si se cumple la condición, devuelve las ordenes a ejecutar
   if p[3] == True:
      p[0] = ['IF', p[6]]


# Definición de ifelse
def p_ifelse(p):
   """ funcionreservada : IFELSE PARENTESISIZQ condicion PARENTESISDER CORCHETEIZQ ordenes CORCHETEDER CORCHETEIZQ ordenes CORCHETEDER PYC
   """
   # Si se cumple la condición, devuelve las ordenes a ejecutar
   if p[3] == True:
      p[0] = ['IFELSE', p[6]]
   else:
      p[0] = ['IFELSE', p[9]]


#################### CICLOS #################### 

# Definición de until
def p_until(p):
   """ funcionreservada : UNTIL CORCHETEIZQ ordenes CORCHETEDER CORCHETEIZQ condicionciclo CORCHETEDER PYC
                                          | UNTIL CORCHETEIZQ ordenes CORCHETEDER PARENTESISIZQ condicionciclo  PARENTESISDER PYC
   """
   # Devuelve el par ordenado con la respectiva condicion
   p[0] = ['UNTIL', p[3], p[6]]


# Definición de while
def p_while(p):
   """ funcionreservada : WHILE  CORCHETEIZQ condicionciclo CORCHETEDER CORCHETEIZQ ordenes CORCHETEDER PYC
                                          | WHILE PARENTESISIZQ condicionciclo PARENTESISDER CORCHETEIZQ ordenes CORCHETEDER PYC
   """
   # Devuelve el par ordenado con la respectiva condicion
   p[0] = ['WHILE', p[3], p[6]]


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

   # Regresa las condiciones en forma de lista
   for i in p:
      condicion.append(i)

   # Elimina el condicion[0] = None que no sirve para las evaluaciones
   condicion.pop(0)

   # Devuelve la condición en forma de lista para evaluarla más fácil
   p[0] = condicion
           

#################### PROCEDIMIENTOS ####################

# Definición de procedimientos
def p_funciones(p):
   """ funcion : PARA ID CORCHETEIZQ parametros CORCHETEDER ordenes FIN
                        | PARA MAIN CORCHETEIZQ parametros CORCHETEDER ordenes FIN
                        | PARA MAIN ordenesmain FIN
   """
   
   # Si se le asignan parámetros a MAIN
   if p[2] == 'MAIN' and isinstance(p[4], list):
      lista_errores.append("ERROR: No se pueden asignar parámetros a MAIN")
      p[0] = None

   # Si se crea un main sin parámetros, suma a la variable
   if p[2] == 'MAIN' and len(p) == 5:
      global main
      main = main + 1
      p[0] = ['FUNCION', p[2], p[3]]
      codigo_main.append(p[3])

   # Si ya hay una variable con el nombre del procedimiento que se crea
   if p[2] in variables:
      lista_errores.append("ERROR: No se puede crear el procedimiento en la linea {0} con el nombre de una variable ya asignada".format(p.lineno(2)))
      p[0] = None

   # Si ya hay un procedimiento con el nombre del procedimiento que se crea
   if p[2] in funciones:
      lista_errores.append("ERROR: No se puede crear el procedimiento en la linea {0} con el nombre de un procedimiento ya creado".format(p.lineno(2)))
      p[0] = None
      
   # Si no hay errores
   if len(p) == 8 and p[2] != 'MAIN':
      p[0] = funciones[p[2]] = ['FUNCION', p[2], p[4], p[6]]

   # Se limpian las variables locales
   variables.clear()


# Ordenes (se dan en forma de una lista de listas)
def p_ordenes(p):
    '''ordenes : continue
                       | funcionreservada
                       | add
                       | sentencia
                       | ordenes add
                       | ordenes sentencia
                       | ordenes funcionreservada
                       | ordenes continue
   '''
    # Revisa si hay alguna asignación de variable
    for i in p:
       if isinstance(i, list):
          if i[0] == 'DEF' and i[1] not in (variables_globales or variables):
             variables_globales[i[1]] = i[2]
          elif i[0] == 'DEF' and i[1] in (variables_globales or variables):
             lista_errores.append("ERROR: Se intentó redefinir la variable {0} ya definida en main".format(i[0]))

   # Si es solo un elemento
    if len(p) == 2:
       p[0] = [p[1]]

   # Si es más de una orden, se concatenan
    else:
       p[0] = p[1] + [p[2]]


# Ordenes (se dan en forma de una lista de listas)
def p_ordenesmain(p):
    '''ordenesmain : sentencia
                                | continue
                                | condicion
                                | operadorlogico
                                | operacion
                                | funcionreservada
                                | funcion
                                | ordenesmain sentencia
                                | ordenesmain continue
                                | ordenesmain condicion
                                | ordenesmain operadorlogico
                                | ordenesmain operacion
                                | ordenesmain funcionreservada
                                | ordenesmain funcion
                                
   '''
   # Revisa si hay alguna asignación de variable
    for i in p:
       if isinstance(i, list):
          if i[0] == 'DEF' and i[1] not in variables_globales:
             variables_globales[i[1]] = i[2]
          elif i[0] == 'DEF' and i[1] in variables_globales:
             lista_errores.append("ERROR: Se intentó redefinir la variable {0} ya definida en main".format(i[0]))

   # Si es solo un elemento       
    if len(p) == 2:
       p[0] = [p[1]]

   # Si es más de un elemento, lo concatena
    else:
       p[0] = p[1] + [p[2]]


#################### ERRORES ####################

# Manejo de errores
def p_error(p):
   if p is not None:
      lista_errores.append("Error de sintaxis en el token {0} {1} en la línea {2}".format(p.type, p.value, p.lineno))
      parser.errok()
   else:
      lista_errores.append("Entrada inesperada")
      
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


#################### Funcionalidad del programa ####################


# Función para revisar si hay una variable
def revisar_variable(a):
   var_local = False
   var_global = False
   
   # Si la variable ya existe, le cambia el valor
   if a in variables_globales:
      var_global = True

   # Si la variable ya existe, le cambia el valor
   elif a in variables:
      var_local = True

   # Si la variable no existe en ninguna lista
   else:
      return False

   # Si se encontró en la lista de variables globales
   if var_global == True:
      return variables_globales[a]

   # Si se encontró en la lista de variables locales
   if var_local == True:
      return variables[a]

   
#################### Resultado del parser ####################
print("\n--------- Resultados del parser ---------")

# Crea el printer para poder imprimir tanto en el Shell de Python como en CMD
pp = pprint.PrettyPrinter(indent = 2)

# Implementación para leer un archivo que será el insumo del parser
with open(archivo_programa, 'r') as archivo:
   insumo = archivo.read()
   resultado = parser.parse(insumo)
   pp.pprint(resultado)
