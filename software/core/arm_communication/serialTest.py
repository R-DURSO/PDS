from time import sleep
import arduino_serial

test = arduino_serial.send("2")

iter = 0
while(1):
    if arduino_serial.getwaiting()>0:
        read = arduino_serial.read()
        print("renvoi :  ",read)
        iter = iter + 1
    if iter == 2: 
        break

a = input('choisir un nombre :')

test = arduino_serial.send(a)
iter =  0
while(1):
    while(1):
        if arduino_serial.getwaiting()>0:
            read = arduino_serial.read()
            a
            print("renvoi :  ",read)
            iter = iter + 1
        if read =="end\n" :
            break
    a = input('choisir un nombre :')
    iter = 0
    test = arduino_serial.send(a)

print("fin")

# arduino_serial.send(2)
