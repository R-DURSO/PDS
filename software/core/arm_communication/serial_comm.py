import serial
import time
import serial.tools.list_ports
import os
 
if(os.name == "posix"):
	port = "/dev/ttyACM0"
else: 
	port = serial.tools.list_ports.comports()[0].name
	print(port)
baudrate = 9600

arduino = serial.Serial(port=port,
                        baudrate=baudrate,
                        bytesize=serial.EIGHTBITS,

                        stopbits=serial.STOPBITS_ONE,
                        timeout=5)


def send(msg):

    if arduino.isOpen():
        print("port already opened \n")
    else:
        arduino.open()

    msg = msg.encode()
    arduino.write(msg)
    time.sleep(1)
    data = b''
    while(arduino.in_waiting<=0):
        time.sleep(0.2)
    while(arduino.in_waiting>0):
        data += arduino.readline()
    return data.decode()


time.sleep(8)
print(send("2"))
print(send("3"))
print(send("1"))
#TODO: find a way to catch last message just before the end of the prog.
