#------------------------------ [IMPORT]------------------------------------
import network, time, urequests
from machine import Pin, ADC, PWM , I2C
from utelegram import Bot
from dht import DHT11
from hcsr04 import HCSR04
import utime
from utime import sleep
from ssd1306 import SSD1306_I2C
import framebuf


TOKEN = '5449717220:AAEAsgmk6dhLWx0VcERIYhLDZZ8IberOV5U'


#--------------------------- [OBJETOS]---------------------------------------

ancho = 128
alto = 64


i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(ancho, alto, i2c)


bot = Bot(TOKEN) # Token Bott

hc04 = HCSR04(trigger_pin=4 , echo_pin=5) # Ultrasonido

bombillo  = Pin(15, Pin.OUT) #Bombillo

sensorDHT = DHT11(Pin(2)) # Termico & Humedad

sensorf = ADC (Pin(32)) # Fotocelda

sensorf.atten(ADC.ATTN_11DB)
sensorf.width(ADC.WIDTH_10BIT)

pir=Pin(34,Pin.IN,Pin.PULL_UP) # Movimiento1
pir2=Pin(35,Pin.IN,Pin.PULL_UP) #movimiento2


#----------------------[ CONECTAR WIFI ]---------------------------------------------------------#

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

def map(x):
        #return int((x - 0) * (8000-1800) / (180 - 0) +1800) # v1.19 -- duty_u16(m) -- 0 y 65536
        return int((x - 0) * (125- 25) / (180 - 0) + 25)
    
def buscar_icono(ruta):
            dibujo= open(ruta, "rb")  # Abrir en modo lectura de bist
            dibujo.readline() # metodo para ubicarse en la primera linea de los bist
            xy = dibujo.readline() # ubicarnos en la segunda linea
            x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
            y = int(xy.split()[1])
            icono = bytearray(dibujo.read())  # guardar en matriz de bites
            dibujo.close()
            return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)# Datos y tamaño de la imagen.

#if conectaWifi ("Nubia And Andres", "Nub14*2014"):
if conectaWifi ("Redmi 10", "1234567899"):   

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
    print("ok")
    
    
    while True:
        sensorDHT.measure()
        tem = sensorDHT.temperature()
        hum = sensorDHT.humidity()
        
        distancia=hc04.distance_cm()
        
       
        estado= pir.value()
        estado2= pir2.value()
            
        @bot.add_message_handler("Hola")
        def help(update):
            update.reply(''' ¡Bienvenidos a VIPRESEG! \U0001F600
                         \n Menu Principal \U0001F606 
                         \n Elije una opción:
                         
                    Estado Temperatura:1
                    Estado Humedad: 2
                    Estado Sensor Ultrasonido:3
                    Estado Sensor Fotoselda:4
                    Estado Sensor de movimiento :5
                    
                    LUZ Encendida \U0001F31E:ON
                    LUZ Apagada \U0001F31A:OFF
                    
                    Activar Oled: Monitoreo
                    
                                           
                         
                         \n No olvides que estoy para ayudarte \U0001F609 ''')
            
    #------------------------------------[SENSORES]---------------------------------------------------------------------#
            
      #------------------------------------[Sensor Temperatura]---------------------------------------------------------------------#      
        
        @bot.add_message_handler("1")
        def help(update):
            update.reply("La temperatura es, " + str(tem) + "°c! \U0001F975")
            
                            
            
        @bot.add_message_handler("2")
        def help(update):
            update.reply("La Humedad es, " + str(hum) + "%! \U0001F4A6")
        
      #------------------------------------[Sensor Ultrasonido]---------------------------------------------------------------------#
            
        @bot.add_message_handler("3")
        def help(update):
            distancia=hc04.distance_cm()
            distancia=(int(distancia))
            update.reply("Distancia es igual: "+ str(distancia)+" Centimetros")
        
      #------------------------------------[Sensor Fotocelda]---------------------------------------------------------------------#      
        @bot.add_message_handler("4")
        def help(update):
            
            factor=100/1023
            lectura= sensorf.read()
            ind=lectura*factor
            Intensidad =round(ind)
            if Intensidad <= 6 :
                Intensidad=Intensidad*20
                Intensidad=(int(Intensidad))
                update.reply("Intensidad es, " + str(Intensidad) + "%")
            elif Intensidad >=80:
                Intensidad=Intensidad/20
                Intensidad=(int(Intensidad))
                update.reply("Intensidad es, " + str(Intensidad) + "%")
           
   
      #------------------------------------[Sensor Movimiento]---------------------------------------------------------------------#  
        @bot.add_message_handler("5")
        def help(update):
                       
            if estado == 1:
                update.reply ("Movimiento Sensor 1 ")
                
            else:
                update.reply ("Sin Movimiento S1 ")
                
            if estado2 == 1:
                update.reply ("Movimiento Sensor 2 ")
                
            else:
                update.reply ("Sin MovimientoS2 ")   
                
            
       #------------------------------------[Bombillo]---------------------------------------------------------------------#
        @bot.add_message_handler("ON")
        def help(update):
            bombillo.value(0)
            update.reply("Encendido \U0001F917")
            
        @bot.add_message_handler("OFF")
        def help(update):
            bombillo.value(1)
            update.reply("Apagado \U0001F634")
            
      #----------------------------------------[OLED]----------------------------------------------------------
        @bot.add_message_handler("Monitoreo")
        def help(update):
            update.reply("Activada Oled \U0001F4FA")
            
            while True:    
                oled.blit(buscar_icono("dibujo/vipreseg1.pbm"), 0, 0) # ruta y sitio de ubicación
                oled.show()  #mostrar
                time.sleep(4)
                
            #::::::::::::::::::::Datos Sensor Temperatura, Himedad:::::::::::::
                
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

               
                oled.fill(0)
                oled.text("SENSOR ULTRASONIDO", 0 , 0)
                oled.text("----------------", 0 , 10)
                oled.text("Distancia", 0 , 20) 
                oled.text(str (round(distancia)), 0 ,30)
                oled.text("Metros", 0 , 40) 
                oled.show()
                sleep(2)
                
            #::::::::::::::::::::Datos Sensor Movimiento:::::::::::::

                       
                
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
                ind=lectura*factor
                Intensidad =round(ind)
                if Intensidad <= 6 :
                    Intensidad=Intensidad*20
                    Intensidad=(int(Intensidad))
                elif Intensidad >=80:
                    Intensidad=Intensidad/20
                    Intensidad=(int(Intensidad))                    
                oled.fill(0)
                oled.text("SENSOR-FOTOCELDA", 0 , 0)
                oled.text("----------------", 0 , 10)
                oled.text("La intensidad es", 0 , 20) 
                oled.text(str (round(Intensidad)), 0 ,30)
                oled.text(".Luminacion", 0 , 40) 
                oled.show()
                sleep(2)
                
                break
               
                
                
                
                

        bot.start_loop()
        
          

else:
    print ("Imposible conectar")
    miRed.active (False)

