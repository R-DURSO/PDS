import serial
import serial.tools.list_ports
import time
import os
if(os.name == "posix"):
	port = "/dev/ttyACM0"
else: 
	port = serial.tools.list_ports.comports()[0].name
	print(port)
baudrate = 115200
	
arduino = serial.Serial(port=port, baudrate=baudrate, timeout=0.1)

def send(msg):
	arduino.write(bytes(msg, "utf-8"))
	time.sleep(0.5)
	data = arduino.readline()
	
	return data.decode()

# q = None
# while q != "":
# 	q = input()
# 	r = send(q)
# 	print(f"Réponse: {r}\n")