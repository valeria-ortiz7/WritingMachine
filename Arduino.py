import serial
import time

ser = serial.Serial('/dev/tty.usbmodem14401', baudrate = 9600, timeout=1)


#arduino = serial.Serial()
#arduino.baudrate = 9600
#arduino.port = "/dev/tty.usbmodem14201"
#arduino.open()

while(1):

     time.sleep(5)
     
     s="ContinueUp 180\n"
     ser.write(s.encode("utf-8"))
     arduinoData = ser.readline().decode('ascii')
     print(arduinoData)

     time.sleep(1)

     s="Down \n"
     ser.write(s.encode("utf-8"))
     arduinoData = ser.readline().decode('ascii')
     print(arduinoData)

     time.sleep(1)
     
     s="PosX 180\n"
     ser.write(s.encode("utf-8"))
     arduinoData = ser.readline().decode('ascii')
     print(arduinoData)
     time.sleep(1)
     
     s="ContinueLeft 180\n"
     ser.write(s.encode("utf-8"))
     arduinoData = ser.readline().decode('ascii')
     print(arduinoData)

     time.sleep(1)
     
     s="ContinueDown 90\n"
     ser.write(s.encode("utf-8"))
     arduinoData = ser.readline().decode('ascii')
     print(arduinoData)

     time.sleep(1)

     s="Speed 180\n"
     ser.write(s.encode("utf-8"))
     arduinoData = ser.readline().decode('ascii')
     print(arduinoData)

     time.sleep(1)
     
     s="ContinueRight 90\n"
     ser.write(s.encode("utf-8"))
     arduinoData = ser.readline().decode('ascii')
     print(arduinoData)

     time.sleep(1)

     s="Up \n"
     ser.write(s.encode("utf-8"))
     arduinoData = ser.readline().decode('ascii')
     print(arduinoData)

     time.sleep(1)
     
     s="ContinueDown 90\n"
     ser.write(s.encode("utf-8"))
     arduinoData = ser.readline().decode('ascii')
     print(arduinoData)

     time.sleep(1)
     
     s="ContinueRight 90\n"
     ser.write(s.encode("utf-8"))
     arduinoData = ser.readline().decode('ascii')
     print(arduinoData)

     time.sleep(1)


     s="begin \n"
     ser.write(s.encode("utf-8"))
     arduinoData = ser.readline().decode('ascii')
     print(arduinoData)
     
     time.sleep(3)

     s="ContinueRight 90\n"
     ser.write(s.encode("utf-8"))
     arduinoData = ser.readline().decode('ascii')
     print(arduinoData)

