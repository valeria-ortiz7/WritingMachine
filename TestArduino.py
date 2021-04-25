from interprete import instrucciones
import serial
import time

"""

Writing Machine
Ejecutar: En caso de que se quiera compilar y ejecutar el programa, se corre este archivo

Llamará el resultado del intérprete y solo lo limpiará para enviar a Arduino

"""

# Abre el puerto de Arduino
#arduino = serial.Serial('COM5', 9600, timeout = 5)
ser = serial.Serial('/dev/tty.usbmodem14101', baudrate = 9600, timeout=1)

print("\n--------- Resultados de ejecutar ---------\n")
print(instrucciones)
print("\n")

largo = len(instrucciones)
contador = 0

with open("instrucciones.txt", "w+") as archivo:
    time.sleep(1)
    for instruccion in instrucciones:
        resultado = ""

        if len(instruccion) == 2:
            resultado = instruccion[0] + " " + str(instruccion[1]) + "\n"
            #archivo.write(str(resultado))
            #print(str(resultado))
            s = str(resultado)
        elif len(instruccion) == 3:
            resultado = instruccion[0] + " " + str(instrucciones[contador][1]) + " " + str(instruccion[2]) + "\n"
            #archivo.write(str(resultado))
            #print(str(resultado))
            s = str(resultado)
        else:
            # Si es una lista de listas
            for j in instruccion:
                if len(j) == 2:
                    resultado = j[0] + " " + str(j[1]) + "\n"

                elif len(j) == 3:
                    resultado = j[0] + " " + str(j[1]) + " " + str(
                        j[2]) + "\n"

                #archivo.write(str(resultado))
                #print(str(resultado))
                s = str(resultado)
        ser.write(s.encode("utf-8"))
        arduinoData = ser.readline().decode('ascii')
        print(arduinoData)
        time.sleep(1)
