import serial
import serial.tools.list_ports
import time
import os
if(os.name == "posix"):
	port = "/dev/ttyACM0"
else: 
	port = serial.tools.list_ports.comports()[0].name
	print(port)
baudrate = 9600
	
arduino = serial.Serial(port=port, baudrate=baudrate,                         
						bytesize=serial.EIGHTBITS,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=5)
time.sleep(8)

def send(msg):
    if arduino.isOpen():
        print("port already opened \n")
    else:
        arduino.open()

    msg = msg.encode()
    arduino.write(msg)
    time.sleep(1)

def read():
    data = arduino.readline()
    arduino.reset_input_buffer()
    arduino.reset_output_buffer()
    return data.decode()

def getwaiting():
	return arduino.in_waiting