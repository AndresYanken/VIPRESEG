from machine import Pin,I2C,ADC
from ssd1306 import SSD1306_I2C
from hcsr04 import HCSR04
from dht import DHT11
import time
from utime import sleep
import framebuf


#::::::::::::::::::::Configuracion de objetos Pantalla OLed:::::::::::::
ancho = 128
alto = 64

sensorDHT = DHT11(Pin(2))
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(ancho, alto, i2c)
hc04 = HCSR04(trigger_pin=4 , echo_pin=5)
pir=Pin(34,Pin.IN,Pin.PULL_UP)
pir2=Pin(35,Pin.IN,Pin.PULL_UP)
sensorf = ADC (Pin(32))
sensorf.atten(ADC.ATTN_11DB)
sensorf.width(ADC.WIDTH_10BIT)

print(i2c.scan())

#::::::::::::::::::::Configuracion Pantalla OLed:::::::::::::

def buscar_icono(ruta):
    dibujo= open(ruta, "rb")  # Abrir en modo lectura de bist
    dibujo.readline() # metodo para ubicarse en la primera linea de los bist
    xy = dibujo.readline() # ubicarnos en la segunda linea
    x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
    y = int(xy.split()[1])
    icono = bytearray(dibujo.read())  # guardar en matriz de bites
    dibujo.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)# Datos y tamaño de la imagen.

#::::::::::::::::::::Imagen VIPRESEG:::::::::::::::::::::::

while True:    
    oled.blit(buscar_icono("dibujo/vipreseg1.pbm"), 0, 0) # ruta y sitio de ubicación
    oled.show()  #mostrar
    time.sleep(4)
    
#::::::::::::::::::::Datos Sensor Temperatura, Himedad:::::::::::::
    
    sensorDHT.measure()
    tem = sensorDHT.temperature()
    hum = sensorDHT.humidity()
    oled.fill(0)
    oled.text("SENSOR TERMICO", 0 , 0)
    oled.text("----------------", 0 , 10)
    oled.text("Temperatura", 0 , 20) 
    oled.text(str(round(tem)), 0 ,30)
    oled.text("Humedad %", 0, 40)
    oled.text(str(round(hum)), 0, 50)
    oled.show()
    sleep(2)
    
    
#::::::::::::::::::::Datos Sensor Ultrasonido:::::::::::::

    #sleep(2)
    distancia=hc04.distance_cm()
    oled.fill(0)
    oled.text("SENSOR ULTRASONIDO", 0 , 0)
    oled.text("----------------", 0 , 10)
    oled.text("Distancia", 0 , 20) 
    oled.text(str (round(distancia)), 0 ,30)
    oled.text("Metros", 0 , 40) 
    oled.show()
    sleep(2)
    
#::::::::::::::::::::Datos Sensor Movimiento:::::::::::::

    estado= pir.value()
    estado2= pir2.value()
    sleep(2)
    
    
    if estado or estado2 == 1:
        oled.fill(0)
        oled.text("SENSOR MOVIMIENTO", 0 , 0)
        oled.text("----------------", 0 , 10)
        oled.text("Movimiento S1 ", 0 , 20) 
        oled.text(str (estado), 0 ,30)
        oled.show()
        sleep(2)
    else:
        oled.fill(0)
        oled.text("SENSOR MOVIMIENTO", 0 , 0)
        oled.text("----------------", 0 , 10)
        oled.text("Sin Movimiento S1", 0 , 20) 
        oled.text(str (estado), 0 ,30)
        oled.text("Metros", 0 , 40) 
        oled.show()
        sleep(2)
    if estado2 == 1:
        oled.fill(0)
        oled.text("SENSOR MOVIMIENTO", 0 , 0)
        oled.text("----------------", 0 , 10)
        oled.text("Movimiento S2 ", 0 , 20) 
        oled.text(str (estado2), 0 ,30)
        oled.text("Metros", 0 , 40) 
        oled.show()
        sleep(2)
    else:
        oled.fill(0)
        oled.text("SENSOR-MOVIMIENTO", 0 , 0)
        oled.text("----------------", 0 , 10)
        oled.text("Sin Movimiento S2 ", 0 , 20) 
        oled.text(str (estado2), 0 ,30)
        oled.text("Metros", 0 , 40) 
        oled.show()
        sleep(2)

#::::::::::::::::::::Datos Sensor Fotocelda :::::::::::::
        
    factor=100/1023
    lectura= sensorf.read()
    Intensidad=lectura*factor
    oled.fill(0)
    oled.text("SENSOR-FOTOCELDA", 0 , 0)
    oled.text("----------------", 0 , 10)
    oled.text("La intensidad es", 0 , 20) 
    oled.text(str (round(Intensidad)), 0 ,30)
    oled.text(".Luminacion", 0 , 40) 
    oled.show()
    sleep(2)

    
   
    
        