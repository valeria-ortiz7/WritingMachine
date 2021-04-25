from myparser import num_variables
from myparser import comentarios
from myparser import num_comentarios
from myparser import funciones
from myparser import lista_funciones
from myparser import main
from myparser import lista_errores
from myparser import resultado as AST

# Flag para verificar si hay errores
flag = True

##################### Verificaciones de compilación #####################

# Verifica si hay al menos un comentario   
if num_comentarios == 0:
   flag = False
   lista_errores.append("ERROR: El programa debe tener al menos un comentario")

   
# Verifica si hay al menos una variable 
elif num_variables == 0:
   flag = False
   lista_errores.append("ERROR: El programa debe tener al menos una asignación de variable")


# Si hay comentarios, revisa que haya uno en la primera línea
elif num_comentarios > 0 and AST != None:
   # Si no hay comentario en la primera línea, da error
   if comentarios[0] != AST[0]:
      flag = False
      lista_errores.append("ERROR: El programa debe tener un comentario en la primera línea del código")

   # Si hay comentarios, los elimina porque no son necesarios
   for comentario in comentarios:
      if comentario in AST:
         AST.remove(comentario)


# Verifica que exista un MAIN
elif main == 0:
   print(main)
   flag = False
   lista_errores.append("ERROR: El programa debe tener un procedimiento MAIN") 

# Si hay errores, añade el mensaje de que no se ejecutará hasta que no hayan errores
if len(lista_errores) != 0:
   lista_errores.append("\nNo se puede ejecutar el programa hasta que no hayan errores en el código.\n")
   flag = False

if AST != None:
   AST = list(filter(None, AST))
