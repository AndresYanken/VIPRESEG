from machine import Pin,I2C
from utime import sleep

from ssd1306 import SSD1306_I2C

ancho=128
alto=64


i2c = I2C(0, scl=Pin(22),sda=Pin(21))
oled = SSD1306_I2C(ancho, alto,i2c)

print(i2c.scan())

while True:   
    oled.text("TE AMO",0,0)
    oled.text("NUBIA JAZMIN SAN", 0 ,10)
    oled.text("  <3   ", 0 ,20)
    oled.text("-------------", 0, 30)
    oled.show()
    sleep(2)
    

'''from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from dht import DHT22
from utime import sleep

ancho = 128
alto = 64

sensorDHT = DHT22(Pin(15))
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(ancho, alto, i2c)

print(i2c.scan())


while True:
 
    sensorDHT.measure()
    tem = sensorDHT.temperature()
    hum = sensorDHT.humidity()
    oled.fill(0)
    oled.text("Temperatura", 0 , 0) # columna ---- fila
    oled.text(str(tem), 0 ,10)
    oled.text("Humedad", 0, 20)
    oled.text(str(hum), 0, 30)
    oled.show()
    sleep(2)'''
