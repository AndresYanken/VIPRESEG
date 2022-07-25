from machine import Pin
from utime import sleep
from hcsr04 import HCSR04

hc04 = HCSR04(trigger_pin=4 , echo_pin=5)

while True:
    sleep(0.5)
    distancia=hc04.distance_cm()
    
    print("Distancia es igual: {:02.2f}".format(distancia))
    
