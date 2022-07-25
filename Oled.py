from machine import Pin,I2C
from utime import sleep
from ssd1306 import SSD1306

ancho=128
alto=64

i2c = I2C(0, scl=Pin(22),sda=Pin(21))
oled = SSD1306(ancho, alto,i2c)

print(i2c.scan())