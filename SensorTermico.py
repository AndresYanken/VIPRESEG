from machine import Pin
from utime import sleep
from dht import DHT11

sensorDHT=DHT11(Pin(2))

while True:
    sleep(2)
    sensorDHT.measure()
    tem=sensorDHT.temperature()
    hum=sensorDHT.humidity()
    
    print("Temperatura: ",tem," Humedad: ",hum ,"%")
