from machine import Pin,ADC
from utime import sleep

sensor = ADC (Pin(32))
sensor.atten(ADC.ATTN_11DB)
sensor.width(ADC.WIDTH_10BIT)

while True:
    factor=100/1023
    lectura= sensor.read()
    Intensidad=lectura*factor
    
    if Intensidad <= 6 :
        Intensidad=Intensidad*20
    elif Intensidad >=80:
        Intensidad=Intensidad/20
   
                 
    print("La intensidad es de ",round(Intensidad),".lm")
    sleep(1)
    
    