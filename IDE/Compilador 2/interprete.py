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

# Si hay errores, no se ejecuta nada
if not flag:
   exit()

##################### Procedimientos de evaluación #####################

def asignar_variable(lista, indicador):
   if indicador == "global":
      variables_globales[lista[1]] = lista[2]

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
   for instruccion in codigo_main:
      if instruccion[0] == 'DEF':
         asignar_variable(instruccion, "global")
         
   ##################### Resultados #####################
   print("\nVariables globales almacenadas durante la ejecución:\n",variables_globales)

