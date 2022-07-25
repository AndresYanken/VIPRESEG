from machine import Pin
from utime import sleep

pir=Pin(34,Pin.IN,Pin.PULL_UP)
pir2=Pin(35,Pin.IN,Pin.PULL_UP)

while True:
    estado= pir.value()
    estado2= pir2.value()
    sleep(1)
    
    if estado == 1:
        print ("Movimiento Sensor 1")
    else:
        print ("Sin Movimiento")
    if estado2 == 1:
        print ("Movimiento Sensor 2")
    else:
        print ("Sin Movimiento")   