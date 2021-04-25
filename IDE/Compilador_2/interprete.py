from compilador import flag as flag_compilador
from compilador import AST
from compilador import funciones
from compilador import lista_funciones
from compilador import lista_errores

# Determinar el directorio actual
import os

# Define dónde se va a guardar el TXT de errores
directorio = os.getcwd() + "/error.txt"



# Código que se va a ejecutar
codigo_main = []

# Instrucciones para el Arduino
instrucciones = []

# Lista de variables almacenadas. Guardará las variables creadas en el diccionario como {ID : valor}
variables = {}

# Lista de variables globales almacenadas. Guardará las variables creadas en el diccionario como {ID : valor}
variables_globales = {}

# Lista de vaiables booleanas. Utilizada para verificar el tipo de variable de entrada
variablesbool = {}

# Lista de funciones reservadas
funcion_reservada = ["ContinueUp","ContinueDown","ContinueLeft","ContinueRight","Pos","PosX","PosY","Speed","UseColor"]

# Tipo de variable global o local que se usará como indicador de scope
tipo_variable = "global"

# En caso de llamarse un procedimiento dentro de otro mantiene un contador del numero de procedimientos en la pila
pila_funcion = 0

# En caso de llamarse un procedimiento dentro de otro mantiene una pila con las variables de los procedimientos en pila
pila_variables = []

# Flag global para indicar si se ejecutará o no el programa
flag = True

##################### Procedimientos de evaluación #####################

def asignar_variable(lista, indicador):
   # Almacena las variables definidas como locales o globales segun el indicador
   if indicador == "global":
      variables_globales[lista[1]] = lista[2]

   elif indicador == "local":
      variables[lista[1]] = lista[2]


###################### Procedimientos de ejecucion ################

def until_exe(until):
   # Recibe una lista con las ordenes de la iteracion y la condicion para repetir
   # Revisa el tipo de condicion y luego hace un While con los valores de la condicion
   # Llama a exe con las ordenes
   # Crea y llena la lista con los resultados obtenidos de exe
   recorrido = []

   while revisar_condicion(until[2]) == True:
      for i in exe(until[1]):
         recorrido.append(i)

   if recorrido == []:
      recorrido.append(exe(until[1]))

   return recorrido


def while_exe(while_):
   # Recibe una lista con las ordenes de la iteracion y la condicion para repetir
   # Revisa el tipo de condicion y luego hace un While con los valores de la condicion
   # Llama a exe con las ordenes
   # Crea y llena la lista con los resultados obtenidos de exe
   recorrido = []
   auxiliar = []

   while revisar_condicion(while_[2]) == True:
      for i in exe(while_[1]):
         recorrido.append(i)

   if recorrido != []:
      for i in recorrido:
         for j in i:
            auxiliar.append(j)

      return auxiliar


def repeat_exe(repeat):
   # Recibe las ordenes y el numero de veces a repetirlas
   # Llama a exe con las ordenes
   # Crea y llena la lista con los resultados obtenidos de exe
   recorrido = []
   cont = 0

   while cont < value(repeat[2]):
      for i in exe(repeat[1]):
         recorrido.append(i)
      cont = cont + 1

   return recorrido


def if_exe(if_):
   # Recibe y analiza la condicion del If
   # Llama a exe con las ordenes del If
   # Crea la lista con los resultados de exe
   recorrido = []

   if revisar_condicion(if_[1]) == True:
      for i in exe(if_[2]):
         recorrido.append(i)

   if recorrido != []:
      print("Recorrido If: ", recorrido)
      return recorrido


def ifelse_exe(ifelse):
   # Recibe y analiza la condicion del IfElse
   # Llama a exe con las ordenes del IfElse
   # Crea la lista con los resultados de exe
   recorrido = []

   if revisar_condicion(ifelse[1]) == True:
      for i in exe(ifelse[2]):
         recorrido.append(i)

   else:
      for i in exe(ifelse[3]):
         recorrido.append(i)

   return recorrido


def funcion_exe(funccall):
   # Recibe una lista con el nombre de la funcion las ordenes y los parametros
   global pila_funcion, variables, pila_variables
   recorrido = []

   # Se llema un contador del numero de funciones en pila
   pila_funcion = pila_funcion + 1
   # En caso de que existan variables locales, las almacena en la pila al entrar a otro metodo
   if variables != {}:
      pila_variables.append(variables.copy())

   # Revisa que exista la funcion
   if funccall[1] in funciones:


      for i in funciones[funccall[1]]:

         # Revisa que la funcion tenga el numero de parametros correcto o si existen dos funciones con el mismo nombre cual es la que se esta llamando
         if len(funccall[2]) == len(lista_funciones[i][0]):
            cont = 0

            # Almacena los parametros y los valores con los que se llamaron en la lista de variables locales
            for x in funccall[2]:
               variables[lista_funciones[i][0][cont]] = value(x)
               cont = cont + 1

            # Guarda en la lista del recorrido los resultados de las ordenes ejecutadas
            ordenes = exe(lista_funciones[i][1])

            # Evita lista de lista
            for i in ordenes:
               recorrido.append(i)

   # Al finalizar la ejecucion de un metodo disminuye el numnero en la pila
   pila_funcion = pila_funcion - 1

   # Limpia las variables al terminar de ejecutar un metodo
   variables.clear()

   if pila_variables != []:
      # Si existen variables en la pila, llena la lista de variables locales con las variables del ultimo metodo en pila para terminar su ejecucion,y elimina estas variables de la pila
      variables = pila_variables[-1]
      pila_variables.pop(-1)

   return recorrido


def exe(listtoexe):
   # Recibe una lista de ordenes
   # Analiza el tipo de ordenes en la lista
   # Segun el tipo de orden genera la ejecucion adecuada
   # Crea una lista con los resultados de las ordenes
   recorrido = []

   global tipo_variable, pila_funcion, pila_variables, flag

   # Por cada linea a ejecutar en el código
   for i in listtoexe:
      if isinstance(i, list):

         if i[0] == "Add":
            # Hace la revisión semántica de la entrada
            if analizador_semantico(i, tipo_variable) == False:
               flag = False

            else:
               if i[1] in variables_globales:
                  variables_globales[i[1]] = variables_globales[i[1]] + value(i[2])

               elif i[1] in variables:
                  variables[i[1]] = variables[i[1]] + value(i[2])

         elif i[0] == "DEF":
            # Revisa si la variable existe, si existe, da el error
            if i[1] in variables_globales or i[1] in variables:
               lista_errores.append("ERROR: No se puede definir el valor {1} a la variable {0} debido a que ya esta definida".format(i[1],i[2]))
               flag = False

            # Si no existe, la asigna
            else:
               asignar_variable(i, tipo_variable)

         elif i[0] == "Put":
            # Hace la revisión semántica de la entrada
            if analizador_semantico(i,tipo_variable) == False:
               flag = False

            # Si no hay errores, modifica el valor
            else:
               if i[1] in variables_globales:
                  variables_globales[i[1]] = value(i[2])

               elif i[1] in variables:
                  variables[i[1]] = value(i[2])

         # Ejecuta un if
         elif i[0] == "IF":
            recorrido.append(if_exe(i))

         # Ejecuta un ifelse
         elif i[0] == "IFELSE":
            resultado = ifelse_exe(i)
            print("Resultado IfElse: ", resultado)
            recorrido.append(resultado)

         # Ejecuta un until
         elif i[0] == "Until":
            for j in until_exe(i):
               recorrido.append(j)

         # Ejecuta un while
         elif i[0] == "While":
            while_ejecutado = while_exe(i)
            if while_ejecutado is not None:
               for j in while_ejecutado:
                  recorrido.append(j)

         # Ejecuta un repeat
         elif i[0] == "Repeat":
            # Revisa la semántica
            if analizador_semantico([i[0], i[2]], tipo_variable) == False:
               flag = False

            # Si no hay errores, ejecuta
            else:
               orden_repetida = repeat_exe(i)
               for j in orden_repetida:
                  recorrido.append(j)

         # Si se llama a una función
         elif i[0] == "funccall":
            # Al llamar a un procedimiento cambia el tipo de variable a locales
            tipo_variable = "local"
            funcion_ejecutada = funcion_exe(i)

            for orden in funcion_ejecutada:
               recorrido.append(orden)

            # En caso de no tener procediemientos en pila, el tipo de variable vuelve a ser global y se limpia las variables locales
            if pila_funcion == 0:
               variables.clear()
               tipo_variable = "global"

         else:
            # Verifica si está en una función reservada
            if i[0] in funcion_reservada:
               funcion = []

               # Si es la función Pos X, Y
               if i[0] == "Pos" :
                  if analizador_semantico([i[0],i[1][0],i[1][1]],tipo_variable) == False:
                     flag = False

                  else:
                     funcion.append(i[0])
                     funcion.append(value(i[1][0]))
                     funcion.append(value(i[1][1]))
                     recorrido.append(funcion)

               else:
                  if analizador_semantico([i[0],i[1]],tipo_variable) == False:
                     flag = False

                  else:
                     funcion.append(i[0])
                     funcion.append(value(i[1]))
                     recorrido.append(funcion)

      # Cuando son metodos sencillos como Begin/Up/Down los almacena directamente
      else:
         recorrido.append(i)

   # Retorna la lista con las instrucciones ejecutadas
   return recorrido


########### Procedimientos de utilidad del programa #########################

def revisar_condicion(condicion):
   # Recibe una lista con los datos de la condicion
   # Busca cual es el tipo de condicion Ej: Smaller/Greater/< etc
   # Segun el tipo de condicion revisa los valores de entrada si se cumple la condicion retorna True si no se cumple False
   global tipo_variable, flag

   # Smaller
   if condicion[0] == "Smaller":
      # Analiza semánticamente la condición
      if analizador_semantico(["MayorMenor", condicion[1], condicion[2]], tipo_variable) == False:
         flag = False

      # Verifica semánticamente la condición
      if type(value(condicion[1])) == type(value(condicion[2])):
         if value(condicion[1]) < value(condicion[2]):
            return True
      
      # Si no se cumple
      else:
         return False

   # Greater
   elif condicion[0] == "Greater":
      # Analiza semánticamente la condición
      if analizador_semantico(["MayorMenor",condicion[1],condicion[2]], tipo_variable) == False:
         flag = False
      
      # Verifica semánticamente la condición
      if type(value(condicion[1])) == type(value(condicion[2])):
         if value(condicion[1]) > value(condicion[2]):
            return True
      
      # Si no se cumple
      else:
         return False

   # Equal
   elif condicion[0] == "Equal":
      # Analiza semánticamente la condición
      if analizador_semantico(["Iguales",condicion[1],condicion[2] ],tipo_variable) == False:
         flag = False

      # Verifica semánticamente la condición
      if type(value(condicion[1])) == type(value(condicion[2])):
         if value(condicion[1]) == value(condicion[2]):
            return True

      # Si no se cumple
      else:
         return False

   # Or
   elif condicion[0] == "Or":
      # Revisa las dos condiciones del Or y si alguna se cumple retorna True
      if revisar_condicion(condicion[1]) == True or revisar_condicion(condicion[2]) == True:
         return True

   elif condicion[0] == "And":
      # Revisa las dos condiciones del And y si ambas se cumplen retorna True
      if revisar_condicion(condicion[1]) == True and revisar_condicion(condicion[2]) == True:
         return True

   elif condicion[1] == "<":
      if analizador_semantico(["MayorMenor",condicion[0],condicion[2] ],tipo_variable) == False:
         flag = False
      if value(condicion[0]) < value(condicion[2]):
         return True

   elif condicion[1] == "<=":
      if analizador_semantico(["MayorMenor",condicion[0],condicion[2] ],tipo_variable) == False:
         flag = False

      if value(condicion[0]) <= value(condicion[2]):
         return True

   elif condicion[1] == ">":
      # Analiza semánticamente la condición
      if analizador_semantico(["MayorMenor",condicion[0],condicion[2] ],tipo_variable) == False:
         flag = False

      if value(condicion[0]) > value(condicion[2]):
         return True

   elif condicion[1] == ">=":
      # Analiza semánticamente la condición
      if analizador_semantico(["MayorMenor",condicion[0],condicion[2] ],tipo_variable) == False:
         flag = False

      if value(condicion[0]) >= value(condicion[2]):
         return True

   elif condicion[1] == "=":
      # Analiza semánticamente la condición
      if analizador_semantico(["Iguales",condicion[0],condicion[2] ],tipo_variable) == False:
         flag = False

      if value(condicion[0]) == value(condicion[2]):
         return True

   # En caso de que la condicion no se cumpla retorna False
   else:
      return False


def value(x):
   # Retorna el valor de una variable, en caso de existir o de una operacion
   valor = 1
   if isinstance(x,list):
      if x[1] == "Mult":
         for i in x[2]:
            valor = valor * value(i)
      elif x[1] == "Div":
         valor = value(x[2]) / value(x[3])
      elif x[1] == "Power":
         valor = pow(value(x[2]),value(x[3]))
      elif x[1] == "Substr":
         valor = value(x[2][0]) * 2
         for i in x[2]:
            valor = valor - value(i)
      elif x[1] == "Sum":
         valor = 0
         for i in x[2]:
            valor = valor + value(i)
      return valor

   if x in variables:
      return variables[x]

   elif x in variables_globales:
      return variables_globales[x]

   # Si recibe un valor bool True
   elif x == "True":
      return True

   # Si recibe un valor bool False
   elif x == "False":
      return False

   # Revisa si es un número
   elif isinstance(x,int):
      return x


def analizador_semantico(entrada, indicador):
   # Revisa un valor, en caso de ser una variable revisar si existe y manejar el tipo de variable
   # Parametros: la lista con la indicación actual, el indicador que indica si es en el scope global o local
   # Los metodos que llaman a este metodo si reciben come resultado False,
   # cambian la Flag global a False ya que hay un error semantico

   # Lista con los metodos que pueden recibir variables y si estos manejan o no bools
   bool_aceptado = {'ContinueUp': False,
                    'ContinueLeft': False,
                    'ContinueDown': False,
                    'ContinueRight': False,
                    'Add': False,
                    'Put': True,
                    'Pos': False,
                    'PosX': False,
                    'PosY': False,
                    'Repeat': False,
                    'Speed': False,
                    'MayorMenor': False,
                    'Iguales': True,
                    'Operacion': False
                    }

   # Flag interna del metodo
   flag = True

   # Da la función actual (ContinueUp, Add, etc)
   funcion = entrada[0]
   # Por cada valor en la lista
   for parametro in entrada:
      # No toma en cuenta el primer valor
      if parametro != funcion:
         # Si es global
         if indicador == "global":
            # Si es numero pasa
            if isinstance(parametro, int):
               pass
            # Si es una descripcion de operacion pasa
            elif parametro == "Sum" or parametro == "Substr" or parametro == "Mult" or parametro == "Div" or parametro == "Power":
               pass
            # Si es una lista la maneja segun sus entradas
            elif isinstance(parametro,list):
               if isinstance(parametro[2],list):
                  for i in parametro[2]:
                     if analizador_semantico([parametro[0],i],"global") == False:
                        flag = False
               else:
                  if analizador_semantico(parametro,"global") == False:
                     flag = False

            # Si el parametro no es una variable pero si un bool
            elif parametro == "True" or parametro == "False":
               # Si la funcionn no acepta bools da error
               if bool_aceptado[funcion] == False:
                  lista_errores.append("ERROR: La función {0} no se puede operar con {1} ya que es un valor booleano".format(funcion,parametro))
                  flag = False

            elif parametro in variables_globales:
               # Aquí, si existe, revisa el valor
               if variables_globales[parametro] == "True" or variables_globales[parametro] == "False":
                  # Si es un bool, revisa si la función lo acepta
                  if bool_aceptado[funcion] == False:
                     lista_errores.append("ERROR: La función {0} no se puede operar con {1} ya que es un valor booleano".format(funcion,parametro))
                     flag = False

            # Si la variable no existe en el scope global
            else:
               lista_errores.append("ERROR: La función {0} no se puede operar con el identificador indefinido {1}".format(funcion,parametro))
               flag = False

         # Si está en un scope local
         if indicador == "local":
            # Si es número, pasa
            if isinstance(parametro, int):
               pass

            # Si es una descripcion de operacion pasa
            elif parametro == "Sum" or parametro == "Substr" or parametro == "Mult" or parametro == "Div" or parametro == "Power":
               pass
            # Si es una lista la maneja segun sus entradas
            elif isinstance(parametro,list):
               if isinstance(parametro[2],list):
                  for i in parametro[2]:
                     if analizador_semantico([parametro[0],i],"local") == False:
                        flag = False
               else:
                  if analizador_semantico(parametro,"local") == False:
                     flag = False
            # Si el parametro no es una variable pero si un bool
            elif parametro == "True" or parametro == "False":
               # Si la funcionn no acepta bools da error
               if bool_aceptado[funcion] == False:
                  lista_errores.append("ERROR: La función {0} no se puede operar con {1} ya que es un valor booleano".format(funcion,parametro))
                  flag = False

            # Si existe en las globales
            elif parametro in variables_globales:
               # Aquí, si existe, revisa el valor
               if variables_globales[parametro] == "True" or variables_globales[parametro] == "False":
                  # Si es un bool, revisa si la función lo acepta
                  if bool_aceptado[funcion] == False:
                     lista_errores.append("ERROR: La función {0} no se puede operar con {1} ya que es un valor booleano".format(funcion,parametro))
                     flag = False

            # Si existe en las locales
            elif parametro in variables:
               # Aquí, si existe, revisa el valor
               if variables[parametro] == "True" or variables[parametro] == "False":
                  # Si es un bool, revisa si la función lo acepta
                  if bool_aceptado[funcion] == False:
                     lista_errores.append("ERROR: La función {0} no se puede operar con {1} ya que es un valor booleano".format(funcion,parametro))
                     flag = False

            # Si la variable no existe en ningún scope
            else:
               lista_errores.append("ERROR: La función {0} no se puede operar con el identificador indefinido {1}".format(funcion,parametro))
               flag = False

   return flag


##################### Recorrido del main #####################

# Se recorre el código del AST, si hay
if AST is not None:
   for sentencia in AST:
      if isinstance(sentencia, list):
         # Si se encuentra el main
         if sentencia[0] == 'MAIN':
            # Almacena las ordenes del main por ejecutar
            codigo_main.append(sentencia[1])

   # Filtrar las ordenes para solo ejecutar ordenes validas (elimina producciones de None)
   codigo_main = list(filter(None, codigo_main[0]))

   # Las instrucciones del arduino son los resultados del procedimiento de ejecucion sobre las instrucciones del Main
   instrucciones = exe(codigo_main)

else:
   # Escribe los errores tanto sintácticos como semánticos encontrados en la lista de errores
   with open(directorio, "w+") as archivo_resultado:
      for i in lista_errores:
         archivo_resultado.write(i + '\n')

##################### Ejecución del intérprete #####################

# Si no hay errores sintácticos ni semánticos
if flag and flag_compilador:
   print("\n--------- Resultados del intérprete ---------\n")

   print("Código a interpretar:")
   print(AST)

   print("\nCodigo para arduino:\n", instrucciones)

   # Imprime los procedimientos creados que encontró en el programa con los índices donde se encuentre un procedimiento con este nombre
   print("\nDiccionario de procedimientos creados: \n", funciones)

   ##################### Resultados #####################
   print("\nVariables globales almacenadas durante la ejecución:\n", variables_globales)


# Escribe los errores tanto sintácticos como semánticos encontrados en la lista de errores
with open(directorio, "w+") as archivo_resultado:
   for i in lista_errores:
      archivo_resultado.write(i + '\n')


# Si hay errores, no se ejecuta nada.
if not flag or not flag_compilador:
   exit()
