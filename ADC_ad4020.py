from tkinter import *
import spidev

#_______________DEFINES_________________
#Register access command  (p.27)
WRITE_REG = 0b00010100
READ_REG  = 0b01010100

#Control register bits (p.26)
TURBO_EN      = 1
HIGHZ_EN      = 2
SPAN_COMPR_EN = 3
STATUS_EN     = 4


def ad4020_config(event):
   config_reg = (  0 << TURBO_EN
                 | 0 << HIGHZ_EN
                 | 0 << SPAN_COMPR_EN
                 | 0 << STATUS_EN)
   adc_data = [READ_REG, config_reg]
   ad4020_spi.writebytes(adc_data)
   

ad4020_spi = spidev.SpiDev(1, 0) 
ad4020_spi.mode = 0
ad4020_spi.max_speed_hz = 10000000

#_____________DEFINES END________________ 
root = Tk()
entry = Entry(root, width = 20)

button_config = Button(root, text = "Config")

button_config.bind("<Button-1>", ad4020_config)

button_config.pack()


root.mainloop()
