from time import sleep
import arduino_serial

test = arduino_serial.send("2")

sleep(10)
while(1):
    if arduino_serial.getwaiting()>0:
        read = arduino_serial.read()
        print("renvoi :  ",read)

# arduino_serial.send(2)
