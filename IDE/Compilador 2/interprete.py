from compilador import flag
from compilador import AST
from compilador import funciones
from compilador import lista_funciones

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

# Si hay errores, no se ejecuta nada
if not flag:
   exit()
# Variables Globales
global tipo_variable, PilaFuncion, pilaVariables
tipo_variable = "global"
PilaFuncion = 0
pilaVariables = []
##################### Procedimientos de evaluación #####################

def asignar_variable(lista, indicador):
   if indicador == "global":
      variables_globales[lista[1]] = lista[2]
   elif indicador == "local":
      variables[lista[1]] = lista[2]




###################### Procedimientos de ejecucion ################

def until_exe(until):
   #Recibe una lista con las ordenes de la iteracion y la condicion para repetir
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
   #Recibe una lista con las ordenes de la iteracion y la condicion para repetir
   # Revisa el tipo de condicion y luego hace un While con los valores de la condicion
   # Llama a exe con las ordenes
   # Crea y llena la lista con los resultados obtenidos de exe
   recorrido = []
   while revisar_condicion(while_[2]) == True:
      for i in exe(while_[1]):
         recorrido.append(i)

   if recorrido != []:
      return recorrido


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
   # Recibe y analisa la condicion del If
   # Llama a exe con las ordenes del If
   # Crea la lista con los resultados de exe
   recorrido = []
   if revisar_condicion(if_[1]) == True:
      for i in exe(if_[2]):
         recorrido.append(i)
   if recorrido != []:
      return recorrido


def ifelse_exe(ifelse):
   # Recibe y analisa la condicion del IfElse
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
   global PilaFuncion, variables,pilaVariables
   recorrido = []
   PilaFuncion = PilaFuncion + 1
   if variables != {}:
      pilaVariables.append(variables.copy())
   if funccall[1] in funciones:
      for i in funciones[funccall[1]]:
         if len(funccall[2]) == len(lista_funciones[i][0]):
            cont = 0
            for x in funccall[2]:
               print(variables)
               variables[lista_funciones[i][0][cont]] = value(x)
               cont = cont + 1
            recorrido.append(exe(lista_funciones[i][1]))
   PilaFuncion = PilaFuncion - 1
   variables.clear()
   if pilaVariables != []:
      variables = pilaVariables[-1]
      pilaVariables.pop(-1)
   return recorrido

def exe(listtoexe):
   # Recibe una lista de ordenes
   # Analisa el tipo de ordenes en la lista
   # Crea una lista con los resultados de las ordenes
   recorrido = []
   global tipo_variable,PilaFuncion,pilaVariables
   for i in listtoexe:
      if isinstance(i, list):
         if i[0] == "Add":
            if i[1] in variables_globales:
               variables_globales[i[1]] = variables_globales[i[1]] + i[2]
            else:
               variables[i[1]] = variables[i[1]] + i[2]
         elif i[0] == "DEF":
            asignar_variable(i,tipo_variable)
         elif i[0] == "Put":
            variables[i[1]] = i[2]
         elif i[0] == "IF":
            recorrido.append(if_exe(i))
         elif i[0] == "IFELSE":
            recorrido.append(ifelse_exe(i))
         elif i[0] == "Until":
            recorrido.append(until_exe(i))
         elif i[0] == "While":
            recorrido.append(while_exe(i))
         elif i[0] == "Repeat":
            recorrido.append(repeat_exe(i))
         elif i[0] == "funccall":
            tipo_variable = "local"
            recorrido.append(funcion_exe(i))
            if PilaFuncion == 0:
               variables.clear()
               tipo_variable = "global"
         else:
            if i[0] in funcion_reservada:
               funcion = []
               if i[0] == "Pos" :
                  funcion.append(i[0])
                  funcion.append(value(i[1][0]))
                  funcion.append(value(i[1][1]))
                  recorrido.append(funcion)
               else:
                  funcion.append(i[0])
                  funcion.append(value(i[1]))
                  recorrido.append(funcion)
      else:
         recorrido.append(i)
   return recorrido

def revisar_condicion(condicion):
   if condicion[0] == "Smaller":
      if value(condicion[1]) < value(condicion[2]):
         return True
   elif condicion[0] == "Greater":
      if value(condicion[1]) > value(condicion[2]):
         return True
   elif condicion[0] == "Equal":
      if value(condicion[1]) == value(condicion[2]):
         return True
   elif condicion[0] == "Or":
      if revisar_condicion(condicion[1]) == True or revisar_condicion(condicion[2]) == True:
         return True
   elif condicion[0] == "And":
      if revisar_condicion(condicion[1]) == True and revisar_condicion(condicion[2]) == True:
         return True
   elif condicion[1] == "<":
      if value(condicion[0]) < value(condicion[2]):
         return True
   elif condicion[1] == "<=":
      if value(condicion[0]) <= value(condicion[2]):
         return True
   elif condicion[1] == ">":
      if value(condicion[0]) > value(condicion[2]):
         return True
   elif condicion[1] == ">=":
      if value(condicion[0]) >= value(condicion[2]):
         return True
   elif condicion[1] == "=":
      if value(condicion[0]) == value(condicion[2]):
         return True
   else:
      return False


def value(x):
   # Retorna el valor de una entrada valida
   if x in variables:
      return variables[x]
   elif x in variables_globales:
      return variables_globales[x]
   elif isinstance(x,int):
      return x





##################### Ejecución del intérprete #####################

# Se debe cambiar a if flag ya que solo se ejecutará si no hay errores
if flag:
   print("\n--------- Resultados del intérprete ---------\n")
   print("Código a interpretar:")
   print(AST)
   # Se recorre el código del AST
   for sentencia in AST:
      if isinstance(sentencia, list):
         # Si se encuentra el main
         if sentencia[0] == 'MAIN':
            # Almacena las ordenes del main por ejecutar
            codigo_main.append(sentencia[1])

   # Filtrar las ordenes para solo ejecutar ordenes validas (elimina producciones de None)
   codigo_main = list(filter(None, codigo_main[0]))
   print("\nCódigo a ejecutar del Main: \n",codigo_main)



   # Imprime los procedimientos creados que encontró en el programa con los índices donde se encuentre un procedimiento con este nombre
   print("\nDiccionario de procedimientos creados: \n", funciones)

   ##################### Recorrido del main #####################


   print("\nEjucucion del codigo Main:\n",exe(codigo_main))

   ##################### Resultados #####################
   print("\nVariables globales almacenadas durante la ejecución:\n",variables_globales)



