# Importa el módulo yacc para el compilador
import ply.yacc as yacc

# Pretty Printer
import pprint

# Sys para leer argumentos
import sys

# Generación de números aleatorios
import random

# Si no se da el archivo TXT para correr el programa
if len(sys.argv) != 2:
   exit()

# Define el archivo del programa
archivo_programa = sys.argv[1]

# Se importan los tokens creados en el otro archivo
from lexer import tokens
from lexer import palabras_reservadas

"""
Writing Machine
Parser: Genera el árbol de parseo. Imprime los resultados del parseo.

Para correr el programa:
   1. En CMD "pip install ply" y luego "pip install pyhcl" 

   2. Luego igual en CMD a la ubicación del archivo (cd Documentos o Descargas o c://Users/nombre...) y
   correr "python myparser.py [nombre_archivo].txt" El archivo de lexer.py tiene que estar en la misma carpeta
"""

# Diccionario de funciones almacenadas del programa para mapear
funciones = {}
lista_funciones = []

# Lista de errores del programa
lista_errores = []

# Cantidad de comentarios
comentarios = []

# Verificaciones
main = 0
num_comentarios = 0
num_variables = 0

# Precedencia para asignar a las operaciones
precedence = (
        ('left', 'PLUS', 'RESTA'),
        ('left', 'MULTIPLICACION', 'DIVISION'),
        ('right', 'UMENOS'),
        ('right', 'POTENCIA')
        )

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
                           | speed
                           | begin
                           | usecolor
                           | write
                           | main
                           | funccall
                        
   '''
   p[0] = p[1]

# Definición de  sentencia
def p_sentencia_expr_error(p):
   ''' sentencia : error
   '''
   lista_errores.append("Error de sintaxis antes de {0} la línea {1}".format(p[1].type, p.lineno(1)))

#################### SENTENCIAS ####################

# Definición de asignación
# Output: ['Def', ID, valor]
def p_asignacion_global(p):
   ''' sentencia : DEF ID IGUAL valor PYC
                 | DEF ID IGUAL TRUE PYC
                 | DEF ID IGUAL FALSE PYC
   '''
   # Si se intenta usar una palabra reservada como ID
   if p[2] in palabras_reservadas.values():
      lista_errores.append("ERROR: La variable {0} no se pudo definir en la línea {1} ya que no puede tener el mismo nombre que una palabra reservada".format(p[2], p.lineno(2)))

   # Revisa si no inicia con una letra minúscula
   elif not p[2][0].islower() or isinstance(p[2][0], int):
      lista_errores.append("ERROR: La variable {0} no se pudo definir en la línea {1} ya que debe empezar con una letra minúscula".format(p[2], p.lineno(2)))
      
   #Verifica que la asignación de la variable cumpla con el tamaño
   elif len(p[2]) >= 3 and len(p[2])<= 10:
      global num_variables
      num_variables = num_variables + 1

      # Regresa la lista con la variable creada y su valor
      p[0] = ['DEF', p[2], p[4]]

   # Si no cumple con el tamaño
   else:
      lista_errores.append("ERROR: La variable {0} no se pudo definir en la línea {1} ya que debe tener más de 3 posiciones y menos de 10 posiciones".format(p[2], p.lineno(2)))

# Error de la función DEF
def p_asignacion_global_error(p):
   ''' sentencia : DEF error PYC
   '''
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[1], p.lineno(2)))


# PUT: Le cambia el valor a una variable ya existente
# Output: ['Put', ID, valor]
def p_sentencia_cambio(p):
   ''' put : PUT ID IGUAL oper PYC
   '''
   p[0] = [p[1], p[2], p[4]]

# Error de la función DEF
def p_sentencia_cambio_error(p):
   ''' put : PUT error PYC
   '''
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[1], p.lineno(2)))
   

#################### SENTENCIAS ####################

# Add: Incrementa el valor de una variable
# Output: ['Add', ID] o ['Add', ID, INT/ID]
def p_add(p):
   ''' add : ADD CORCHETEIZQ ID CORCHETEDER PYC
                 | ADD CORCHETEIZQ ID ID CORCHETEDER PYC
                 | ADD CORCHETEIZQ ID INT CORCHETEDER PYC
   '''
   if len(p) == 6:
      p[0] = [p[1], p[3]]

   elif len(p) == 7:
      p[0] = [p[1], p[3], p[4]]

# Error de la función DEF
def p_add_error(p):
   ''' add : ADD error PYC
               | ADD CORCHETEIZQ error CORCHETEDER PYC
               | ADD error CORCHETEDER PYC'''
   
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[1], p.lineno(2)))


# Definición de valor
def p_valor(p):
   ''' valor : INT
                  | ID
   '''
   if isinstance(p[1], int):
      p[0] = p[1]

   else:
      p[0] = str(p[1])
      

#################### FUNCIONES DE DIBUJO ####################

# Definición de Continue
# Output: ['ContinueX', valor/expresion]
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
   p[0] = [p[1], p[2]]

# Error de la función CONTINUE
def p_continue_error(p):
   ''' continue : CONTINUEUP error PYC
                        | CONTINUEDOWN error PYC
                        | CONTINUERIGHT error PYC
                        | CONTINUELEFT error PYC
                        | CONTINUEUP error
                        | CONTINUEDOWN error 
                        | CONTINUERIGHT error 
                        | CONTINUELEFT error 
   '''
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[1], p.lineno(2)))


# Definicion de Pos
# Output: [Pos, [X,Y]]
def p_pos(p):
   ''' pos : POS CORCHETEIZQ parametros CORCHETEDER PYC
               | POSX expresion PYC
               | POSX valor PYC
               | POSY expresion PYC
               | POSY valor PYC
   '''
   # Si es Pos[X, Y]
   if len(p) == 6:
      p[0] = [p[1], p[3]]
   else:
      p[0] = [p[1], p[2]]

# Error de la función POS
def p_pos_error(p):
   ''' pos : POS error PYC
               | POSX error PYC
               | POSY error PYC
   '''
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[1], p.lineno(2)))


# Definición de Write
# Output: Down o Up
def p_write(p):
   '''write : DOWN PYC
                | UP PYC
   '''
   p[0] = p[1]

# Error de la función WRITE
def p_write_error(p):
   ''' write : DOWN
                  | UP
   '''
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}, falta un ';'".format(p[1], p.lineno(1)))


# Definicion de UseColor
# Output: ['UseColor', valor]
def p_usecolor(p):
   '''usecolor : USECOLOR valor PYC
                      | USECOLOR expresion PYC
   '''
   if isinstance(p[2], int):
      if 1 <= p[2] <= 3:
         p[0] = [p[1] , p[2]]
         
      else:
         lista_errores.append("ERROR: Los valores aceptados para UseColor son 1, 2 o 3. Se utilizó {0} en la linea {1}".format(p[2], p.lineno(1)))
         p[0] = None

   else:
      p[0] = [p[1], p[2]]

# Error de la función UseColor
def p_usecolor_error(p):
   ''' usecolor : USECOLOR error
                        | USECOLOR error PYC
   '''
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[1], p.lineno(2)))


#################### Funciones de control de la maquina ####################

# Definicion de Begin
def p_begin(p):
   '''begin : BEGIN PYC
   '''
   p[0] = p[1]

# Error de la función Begin
def p_begin_error(p):
   ''' begin : BEGIN
                  | BEGIN error PYC
   '''
   if len(p) == 4:
      lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}. La función {0} no recibe parámetros".format(p[1], p.lineno(2)))

   else:
      lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[1], p.lineno(1)))


# Definicion de Speed
def p_speed(p):
   '''speed : SPEED expresion PYC
                  | SPEED valor PYC
   '''
   p[0] = [p[1], p[2]]

# Error de la función Speed
def p_speed_error(p):
   ''' speed : SPEED error PYC
   '''
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[1], p.lineno(2)))
   

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


# Número negativo error
def p_expresion_menos_error(p):
   '''expresion : RESTA error'''
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[2], p.lineno(1)))


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
   """ condicion : oper MAYORQUE oper
                            | oper MENORQUE oper
                            | oper MENOROIGUAL oper
                            | oper MAYOROIGUAL oper
                            | oper IGUAL oper
   """
   p[0] =[p[1], p[2], p[3]]

# Operador de funciones
def p_operadorcondicion(p):
   ''' oper : valor
                 | expresion
   '''
   if isinstance(p[1], int):
      p[0] = p[1]
   else:
      p[0] = str(p[1])

#################### COMPARADORES ####################

# Definición de Equal
def p_equal(p):
   """ condicion : EQUAL PARENTESISIZQ oper COMA oper PARENTESISDER PYC
   """
   p[0] = [p[1], p[3], p[5]]

# Definición de Greater
def p_greater(p):
   """ condicion : GREATER PARENTESISIZQ oper COMA oper PARENTESISDER PYC
   """
   p[0] = [p[1], p[3], p[5]]

# Definición de Smaller
def p_smaller(p):
   """ condicion : SMALLER PARENTESISIZQ oper COMA oper PARENTESISDER PYC
   """
   p[0] = [p[1], p[3], p[5]]


# Error de la función Condición y Comparadores
def p_condicion_error(p):
   ''' condicion : error MAYORQUE error
                            | error MENORQUE error
                            | error MENOROIGUAL error
                            | error MAYOROIGUAL error
                            | error IGUAL error
                            | EQUAL error PYC
                            | SMALLER error PYC
                            | GREATER error PYC
   '''
   if p[1] == "Equal" or p[1] == "Smaller" or p[1] == "Greater":
      lista_errores.append("ERROR: Error de sintaxis en la condición {0} en la línea {1}".format(p[1], p.lineno(2)))

   else:
      lista_errores.append("ERROR: Error de sintaxis en la condición {0} en la línea {1}".format(p[2], p.lineno(1)))


#################### OPERADORES LÓGICOS ####################

# Definición de And
def p_and(p):
   """ operadorlogico : AND PARENTESISIZQ condicion COMA condicion PARENTESISDER PYC 
   """
   p[0] = [p[1], p[3], p[5]]


# Definición de Or
def p_or(p):
   """ operadorlogico : OR PARENTESISIZQ condicion COMA condicion PARENTESISDER PYC 
   """
   p[0] = [p[1], p[3], p[5]]

# Error de los operadores lógicos
def p_operadorlogico_error(p):
   ''' operadorlogico : OR error PYC
                                     | AND error PYC
   '''
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[1], p.lineno(2)))


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

# Error de las operaciones
def p_operacion_error(p):
   ''' operacion : MULT error PYC
                           | SUM error PYC
                           | DIV error PYC
                           | POWER error PYC
                           | RANDOM error PYC
                           | SUBSTR error PYC
   '''
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[1], p.lineno(2)))

#################### PARAMETROS ####################


# Parametros (se dan en forma de una lista)
def p_parametros(p):
    '''parametros : expresion
                             | valor
                             | parametros COMA oper
    '''

    # Si es solo una expresion
    if len(p) == 2:
       p[0] = [p[1]]

    # Si son más de dos
    else:
       p[0] = p[1] + [p[3]]


#################### FUNCIONES INTERNAS ####################

# Definición de run
def p_run(p):
   ''' funcionreservada : RUN CORCHETEIZQ ordenes CORCHETEDER PYC
   '''
   # Solo devuelve las órdenes a ejecutar
   p[0] = p[3]


# Definición de Repeat
def p_repeat(p):
   ''' funcionreservada : REPEAT valor CORCHETEIZQ ordenes CORCHETEDER PYC
   '''
   # Devuelve las ordenes a ejecutar y numero de veces que debe hacerlo
   p[0] = [p[1] , p[4], p[2]]

#################### EVALUACIONES #################### 

# Definición de if
def p_if(p):
   ''' funcionreservada : IF PARENTESISIZQ condicion PARENTESISDER CORCHETEIZQ ordenes CORCHETEDER PYC
   '''
   p[0] = ['IF', p[3], p[6]]


# Definición de ifelse
def p_ifelse(p):
   ''' funcionreservada : IFELSE PARENTESISIZQ condicion PARENTESISDER CORCHETEIZQ ordenes CORCHETEDER CORCHETEIZQ ordenes CORCHETEDER PYC
   '''
   # Si se cumple la condición, devuelve las ordenes a ejecutar
   p[0] = ['IFELSE', p[3], p[6], p[9]]

# Definición de errores de las funciones reservadas IF, IFELSE, RUN, REPEAT
def p_funcionreservada_error(p):
   ''' funcionreservada : IF error PYC
                                       | IFELSE error PYC
                                       | REPEAT error PYC
                                       | RUN error PYC
   '''
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[1], p.lineno(2)))

#################### CICLOS #################### 

# Definición de until
# Output: ['Until', ordenes, condicion]
def p_until(p):
   ''' funcioniter : UNTIL CORCHETEIZQ ordenes CORCHETEDER CORCHETEIZQ condicion CORCHETEDER PYC
                             | UNTIL CORCHETEIZQ ordenes CORCHETEDER PARENTESISIZQ condicion  PARENTESISDER PYC
   '''
   # Retorna la informacion necesaria para su evaluacion
   p[0] = [p[1], p[3], p[6]]


# Definición de while
# Output: ['Until', condicion, ordenes]
def p_while(p):
   ''' funcioniter : WHILE  CORCHETEIZQ condicion CORCHETEDER CORCHETEIZQ ordenes CORCHETEDER PYC
                               | WHILE PARENTESISIZQ condicion PARENTESISDER CORCHETEIZQ ordenes CORCHETEDER PYC
   '''
   # Retorna la informacion necesaria para su evaluacion
   p[0] = [p[1], p[6], p[3]]

# Definición de errores de las funciones iterativas WHILE, UNTIL
def p_funcionreservada_error(p):
   ''' funcionreservada : WHILE error PYC
                                       | UNTIL error PYC
   '''
   lista_errores.append("ERROR: Error de sintaxis en la función {0} en la línea {1}".format(p[1], p.lineno(2)))


#################### PROCEDIMIENTOS ####################

# Definición de procedimientos

def p_funciones(p):
   ''' funcion : PARA ID CORCHETEIZQ parametros CORCHETEDER CORCHETEIZQ ordenes CORCHETEDER FIN
   '''
   # Si se intenta usar una palabra reservada como ID
   if p[2] in palabras_reservadas.values():
      lista_errores.append("ERROR: La función {0} no se pudo definir en la línea {1} ya que no puede tener el mismo nombre que una palabra reservada".format(p[2], p.lineno(2)))

   # Si no hay ningún procedimiento definido con este nombre
   if p[2] not in funciones:      
      funciones[p[2]] = [len(lista_funciones)]
      lista_funciones.append([p[4], p[7]]) 

   # Si ya existe un procedimiento con este nombre
   elif p[2] in funciones:
      flag = True
      
      # Busca el procedimiento en el diccionario y la posición que tiene en la lista de funciones
      for i in funciones[p[2]]:
         # Verifica en la lista de funciones si aparte de tener el mismo nombre, tienen la misma cantidad de parámetros
         if len(lista_funciones[i][0]) == len(p[4]):
            lista_errores.append("ERROR: La función {0} no se pudo definir en la línea {1} ya que está duplicada".format(p[2], p.lineno(2)))

            # Define el flag como falso para que no se agregue luego la función a la lista en caso de estar duplicado
            flag = False

      # Si se determina que los parámetros son diferentes, la agrega a la lista
      if flag == True:
         funciones[p[2]] = funciones[p[2]] + [len(lista_funciones)]
         lista_funciones.append([p[4], p[7]]) 
      

# Definición de errores para los procedimientos
def p_funciones_error(p):
   ''' funcion : PARA error PYC
   '''
   lista_errores.append("ERROR: Error de sintaxis en la definición de procedimiento en la línea {0}".format(p.lineno(2)))
   

# Definición de MAIN
def p_main(p):
   ''' main : PARA MAIN CORCHETEIZQ ordenes CORCHETEDER FIN
   '''
   global main

   if main != 0:
      lista_errores.append("ERROR: No puede haber más de una definición de Main, se encontró otra definición en la línea {0}".format(p.lineno(2)))

   else:
      main = main + 1
      p[0] = [p[2], p[4]]

# Definición de errores de MAIN
def p_main_error(p):
   ''' main : PARA MAIN error FIN
                 | PARA MAIN error CORCHETEIZQ ordenes CORCHETEDER FIN
                 | PARA MAIN CORCHETEIZQ error CORCHETEDER CORCHETEIZQ ordenes CORCHETEDER FIN
   '''
   if len(p) == 5:
      lista_errores.append("ERROR: Error en la definición de Main en la línea {0}.".format(p.lineno(3)))

   else:
      lista_errores.append("ERROR: Error en la definición de Main en la línea {0}. Main no puede incluir parámetros".format(p.lineno(3)))
      

# Definicion de llamadas de funciones
# Output : [nombre_funcion, parametros]
def p_funccall(p):
   """ funccall : ID CORCHETEIZQ parametros CORCHETEDER PYC"""
   p[0] = ['funccall', p[1], p[3]]
   

# Ordenes (se dan en forma de una lista de listas)
def p_ordenes(p):
    '''ordenes : continue
               | funcionreservada
               | add
               | pos
               | operacion
               | put
               | funccall
               | sentencia
               | funcioniter
               | ordenes add
               | ordenes funccall
               | ordenes sentencia
               | ordenes funcionreservada
               | ordenes continue
               | ordenes funcioniter
               | ordenes put
               | ordenes pos
               | ordenes operacion
   '''

   # Si es solo un elemento
    if len(p) == 2:
       p[0] = [p[1]]

   # Si es más de una orden, se concatenan
    else:
       p[0] = p[1] + [p[2]]

#################### PARSER ####################   
   
# Construye el parser
parser = yacc.yacc()

# Crea el printer para poder imprimir tanto en el Shell de Python como en CMD
pp = pprint.PrettyPrinter(indent = 2)

# Implementación para leer un archivo que será el insumo del parser
with open(archivo_programa, 'r') as archivo:
   insumo = archivo.read()
   resultado = parser.parse(insumo)

   # Elimina las producciones vacías (None)
   if resultado != None:
      resultado = list(filter(None, resultado))

   # Imprime el resultado del parser
   print("\n--------- Resultados del parser ---------")
   pp.pprint(resultado)
