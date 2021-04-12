from myparser import codigo_main
from myparser import num_comentarios
from myparser import num_variables
from myparser import comentarios
from myparser import main
from myparser import resultado
from myparser import variables_globales
from myparser import variables
from myparser import lista_errores
import pprint
import os

"""

Writing Machine
Compilador: Escribe los errores en el TXT

Para correr el programa:
   1. En CMD "pip install ply" y luego "pip install pyhcl" 
   2. Luego igual en CMD a la ubicación del archivo (cd Documentos o Descargas o c://Users/nombre...) y
   correr "python compilador.py" El archivo de lexer.py, parser.py y entrada.txt tiene que estar en la misma carpeta

"""

# Define las instrucciones que serán evaluadas
instrucciones = []
directorio = os.getcwd() + "/Compilador/error.txt"
print(os.getcwd())

# Elimina las ordenes vacías del main
for ordenes in codigo_main:
   for orden in ordenes:
      if orden == None:
         ordenes.remove(orden)


# Flag para verificar si hay identificadores y comentarios
flag = True


# Verifica si hay al menos un comentario   
if num_comentarios == 0:
   flag = False
   lista_errores = []
   lista_errores.append("ERROR: El programa debe tener al menos un comentario")

   
# Verifica si hay al menos una variable 
if num_variables == 0:
   flag = False
   lista_errores = []
   lista_errores.append("ERROR: El programa debe tener al menos una asignación de variable")


# Si hay comentarios, revisa que haya uno en la primera línea
if num_comentarios > 0 and resultado != None:
   # Si no hay comentario en la primera línea, da error
   if comentarios[0] != resultado[0]:
      flag = False
      lista_errores = []
      lista_errores.append("ERROR: El programa debe tener un comentario en la primera línea del código")

   # Si hay comentarios, los elimina porque no son necesarios
   for comentario in comentarios:
      if comentario in resultado:
         resultado.remove(comentario)


# Verifica que exista un MAIN
if main == 0:
   flag = False
   lista_errores = []
   lista_errores.append("ERROR: El programa debe tener un procedimiento MAIN")


# Verifica que exista únicamente un MAIN
if main > 1:
   flag = False
   lista_errores = []

   lista_errores.append("ERROR: Únicamente puede haber un procedimiento llamado MAIN")

# Si no hay errores de sintaxis
if resultado != None and flag == True:
   print("\n--------- Resultados del compilador ---------")
   print("Variables globales: {0} ".format(variables_globales))
   print("Variables locales: {0} ".format(variables))


# Si no hay errores
### SE DEBE CAMBIAR A ----> if len(lista_errores) == 0:
if len(lista_errores) != 0:
   instrucciones = codigo_main

# Escribe los errores encontrados en la lista de errores
with open(directorio, "w+") as archivo_resultado:
   for i in lista_errores:
      archivo_resultado.write(i + '\n')
