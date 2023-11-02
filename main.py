# Autor: Roman Castro Christopher Alexander 
# Contacto: l20211837@tectijuana.edu.mx
# Fecha: 2023-10-16
# Descripción: Código que muestra la temperatura en un dispositivo I2C y muestra diferentes imágenes en el mismo dependiendo de la temperatura detectada por el controlador integrado en la Raspberry Pi Pico.

# Display Image & text on I2C driven ssd1306 OLED display 
from machine import Pin, I2C
import ssd1306
import framebuf
import machine
import utime


sensor_temp = machine.ADC(4)

# Configuración de la pantalla OLED SSD1306 a través de I2C
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=400000)

oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Función para leer la temperatura en grados Celsius
def obtener_temperatura():
    lectura = sensor_temp.read_u16() * 3.3 / (65535)
    temperatura = 27 - (lectura - 0.706) / 0.001721
    return temperatura

# Función para mostrar imágenes temáticas según la temperatura
def mostrar_imagen_temperatura(temperatura):
    temp = ''
    if temperatura < 22.899:
        # Mostrar imagen de frío
        imagen = bytearray(b'\x00\x00\x00\x00\x00\nJ\x00\x00 \x00\x00\x08\xc2\x00\x88\x03)H@$\xa4\x91 \t\x15$\x08IRID\x12)\x14\x80@\xaaJj$\x91%\x10)*\x99TBy^\xa4Yz^JJZ\xbd"*\xba]JUR\x8a\x02T\x89UhR\xb5U\n-\xaa\xaa\xd4*\x00\x00T*\x00\x10,\x14\xaa\x85P\x1a\x00\x10X\n\x89\x12\xa0\n\xf6\xedP\x05*\x95@\x02\xd5\xc3@\x10V-\x00\x00\x15\xd0\x02\x00\x00\x00\x00\x00\x80\x00\x08')
        temp = 'frio'
        
    elif 22.899 <= temperatura < 23.699:
        # Mostrar imagen de cálido
        imagen = bytearray(b'\x00\x00\x00\x00\x00\x15P\x00\x00\x1f\xf8\x00\x00\xe0\x07\x00\x01\x80\x01\x80\x02\t$\x80\x06@\x00`\x0c\x00@0\x10=\x1f\x08\x18\xd6*\x98\x10\xc2 \x88b\xd35\x86 \xc2 \x94`V5\x86$<\x1f\x04`\x80\x80\x06`\x80\x80\x06"\x00\x00$`\x08D\x86 \x82\x00\x04d\xc8\x13\x16\x10\xc0\x83\x08\x18`\n\x18\x11$DH\x0c\x18\x180\x02\x0f\xf1@\x03\x05\xa0\xc0\x01\xa0\x05\x80\x00\xe0\x06\x00\x00\x1f\xf8\x00\x00\x16\xd0\x00\x00\x00\x00\x00')
        temp = 'templado'
    else:
        # Mostrar imagen de caliente
        imagen = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x04@\x00\x00\x00\x00\x00\x02\x80\x02@\x00\n\x90\x00\x02\x00\x00\x80\x00*\xa0\x00\x00\x10\x08\x00\x00\xa5\x02\x00\x00\x00H\x00\x08\xaa\x00\x00\x00\x80J \x14T\x00\x10\x00\x82\xa2 \x08(\x08\x00\x00\x92B\x00\x00H\x91\x00\x00$\x08\x00\x00\tP\x00\x02\x12@@\x00\x00\x10\x80\x02\x80\x02\x00\x00\x05\x00\x00\x00\x00\x80\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        temp = 'caliente'
    
    fb = framebuf.FrameBuffer(imagen, 32, 32, framebuf.MONO_HLSB)
    
    oled.fill(0)
    
    oled.blit(fb, 2, 0)
    oled.text('Temp: {} C'.format(temperatura), 0, 46)
    oled.show()
    
    

# Bucle principal para medir la temperatura y mostrar la imagen

#while True:
temp = obtener_temperatura()
print('Temperatura actual: {} °C'.format(temp))    
mostrar_imagen_temperatura(temp)
utime.sleep(3)  # Pausa de 5 segundos entre las mediciones
