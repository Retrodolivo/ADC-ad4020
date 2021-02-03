from tkinter import *
import time
import spidev
import RPi.GPIO as GPIO


#_______________DEFINES_________________
#Register access command  (p.27)
WRITE_REG = 0b00010100
READ_REG  = 0b01010100

#Control register bits (p.26)
TURBO_EN      = 1
HIGHZ_EN      = 2
SPAN_COMPR_EN = 3
STATUS_EN     = 4

BUTTON_CNV = 23

#SPI1 configuraton  
ad4020_spi = spidev.SpiDev(1, 0) 
ad4020_spi.mode = 0
ad4020_spi.max_speed_hz = 10000000

# GPIO numbering, not a pin numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_CNV, GPIO.OUT, GPIO.PUD_OFF, GPIO.LOW)


def ad4020_config(event):
   config_reg = (  0 << TURBO_EN
                 | 0 << HIGHZ_EN
                 | 0 << SPAN_COMPR_EN
                 | 0 << STATUS_EN)
   adc_data = [READ_REG, config_reg]
   ad4020_spi.writebytes(adc_data)

def read_routine():
   read_val = 0
   read_val = read_val.to_bytes(3, "big")
   read_val = ad4020_spi.xfer(read_val)
   print(read_val)

def ad4020_read(event):
   GPIO.output(BUTTON_CNV, GPIO.HIGH)
   GPIO.output(BUTTON_CNV, GPIO.LOW)
   read_routine()

def close(event):
   GPIO.cleanup()
   root.destroy()
   

#_____________DEFINES END________________ 
root = Tk()
entry = Entry(root, width = 20)

button_config = Button(root, text = "Config")
button_read = Button(root, text = "Read")
button_exit = Button(root, text = "Exit")

button_config.bind("<Button-1>", ad4020_config)
button_read.bind("<Button-1>", ad4020_read)
button_exit.bind("<Button-1>", close)

button_config.pack()
button_read.pack()
button_exit.pack()

root.mainloop()



