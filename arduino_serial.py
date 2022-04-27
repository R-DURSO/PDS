import serial
import time

port = "/dev/ttyACM0"
baudrate = 115200

arduino = serial.Serial(port=port, baudrate=baudrate, timeout=0.1)

def send(msg):
	arduino.write(bytes(msg, "utf-8"))
	time.sleep(0.5)
	data = arduino.readline()
	
	return data

q = None
while q != "":
	q = input()
	r = send(q)
	print(f"Réponse: {r}\n")