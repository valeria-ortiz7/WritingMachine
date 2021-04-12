from compilador import instrucciones
import serial
import time

"""

Writing Machine
Ejecutar: En caso de que se quiera compilar y ejecutar el programa, se corre este

Aún no hace nada, se deben agregar las evaluaciones de todo y escribir al Arduino

Para correr el programa:
   1. En CMD "pip install ply" y luego "pip install pyhcl" 
   2. Luego igual en CMD a la ubicación del archivo (cd Documentos o Descargas o c://Users/nombre...) y
   correr "python ejecutar.py" El archivo de lexer.py, parser.py y entrada.txt tiene que estar en la misma carpeta

"""

# Abre el puerto de Arduino
arduino = serial.Serial('COM5', 9600, timeout = 5)
time.sleep(5)

print("\n--------- Resultados de ejecutar ---------")
instrucciones = instrucciones[0]

# Envía cada instrucción a Arduino para que la ejecute
while len(instrucciones) != 0:
   for i in instrucciones:
      # Elimina la instrucción
      instrucciones.remove(i)

"""
valor = str(i)
print ("Valor enviado por Python: ")
print (valor)
arduino.write(str.encode(valor))
time.sleep(4)
instrucciones.remove(i)
#ard.close()
"""
