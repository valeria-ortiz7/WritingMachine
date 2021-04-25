from interprete import instrucciones
import serial
import time

"""

Writing Machine
Ejecutar: En caso de que se quiera compilar y ejecutar el programa, se corre este archivo

Llamará el resultado del intérprete y solo lo limpiará para enviar a Arduino

"""

# Abre el puerto de Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
done = False

while True:

    if not done:
        for instruccion in instrucciones:
            resultado = ""

            if len(instruccion) == 2:
                resultado = instruccion[0] + " " + str(instruccion[1]) + "\n"
                arduino.write(resultado.encode())
                time.sleep(0.5)

            elif len(instruccion) == 3:
                resultado = instruccion[0] + " " + str(instruccion[1]) + " " + str(instruccion[2]) + "\n"
                arduino.write(resultado.encode())
                time.sleep(0.5)

            else:
                # Si es una lista de listas
                for j in instruccion:
                    if len(j) == 2:
                        resultado = j[0] + " " + str(j[1]) + "\n"
                        arduino.write(resultado.encode())
                        time.sleep(0.5)

                    elif len(j) == 3:
                        resultado = j[0] + " " + str(j[1]) + " " + str(
                            j[2]) + "\n"
                        arduino.write(resultado.encode())
                        time.sleep(0.5)

            leer = arduino.readline().decode('ascii')
            time.sleep(0.5)

        done = True

    else:
        break

time.sleep(2)
arduino.close()

print("\n--------- Resultados de ejecutar ---------\n")
print(instrucciones)
print("\n")
