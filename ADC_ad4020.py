from tkinter import *
import time
import spidev
import numpy
import RPi.GPIO as GPIO


#_______________DEFINES_________________
###TOGGLE PRINT TO SHELL###
PRINTENABLE = 1
########################
VREF_POS = 5
VREF_NEG = -5

MAX_CODE = 2**19 - 1

#Register access command  (p.27)
WRITE_REG = 0b00010100
READ_REG  = 0b01010100

#Control register bits (p.26)
TURBO_EN      = 1
HIGHZ_EN      = 2
SPAN_COMPR_EN = 3
STATUS_EN     = 4

PIN_CNV = 23

#SPI configuraton
def ad4020_spi_init(port, cs, mode, speed):
    ad4020_spi = spidev.SpiDev(port, cs) 
    ad4020_spi.mode = mode
    ad4020_spi.max_speed_hz = speed

# GPIO numbering, not a pin numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_CNV, GPIO.OUT, GPIO.PUD_OFF, GPIO.LOW)


def ad4020_config(event):
    config_reg = (  0 << TURBO_EN
                  | 0 << HIGHZ_EN
                  | 0 << SPAN_COMPR_EN
                  | 0 << STATUS_EN)
    adc_data = [READ_REG, config_reg]
    ad4020_spi.writebytes(adc_data)


def diff_to_single(vref, vdiff):
    e1 = numpy.array([[1., 1.], [1., -1]])
    e2 = numpy.array([vref, vdiff])
    if vdiff > 0:
        return numpy.linalg.solve(e1, e2)[0]
    else:
        return -(numpy.linalg.solve(e1, e2)[0])

def ad4020_read(event):
    raw_code = 0

    #Make a pulse on CNV pin to start conversion
    GPIO.output(PIN_CNV, GPIO.HIGH)
    GPIO.output(PIN_CNV, GPIO.LOW)

    raw_code = raw_code.to_bytes(3, "big")
    raw_code = ad4020_spi.xfer(raw_code)
    #fit raw data to 20 bit value
    code = ( raw_code[0] << 12 |
             raw_code[1] << 4   |
             raw_code[2] >> 4)

    LOWEST_POS_CODE = 0x00001
    HIGHEST_POS_CODE = 0x7FFFF
    LOWEST_NEG_CODE = 0x80000
    HIGHEST_NEG_CODE = 0xFFFFF
   
    if code >= LOWEST_POS_CODE and code <= HIGHEST_POS_CODE:
        voltage_diff = float(code) / MAX_CODE * VREF_POS
        if PRINTENABLE:
            print("voltage_in: %.3f" %(diff_to_single(VREF_POS, voltage_diff)))
            return diff_to_single(VREF_POS, voltage_diff)
        else:
            return diff_to_single(VREF_POS, voltage_diff)
    

      
    if code >= LOWEST_NEG_CODE and code <= HIGHEST_NEG_CODE:
        voltage_diff = float(code) / MAX_CODE * VREF_NEG
        if PRINTENABLE:
            print("voltage_in: %.3f" %(diff_to_single(VREF_POS, voltage_diff)))
            return diff_to_single(VREF_POS, voltage_diff)
        else:
            return diff_to_single(VREF_POS, voltage_diff)

    if PRINTENABLE:
        print("Voltage_diff: %.3f" %(voltage_diff))   
        print(raw_code)
        print(code)
        
def close(event):
    GPIO.cleanup()
    root.destroy()
   

#_____________DEFINES END________________
if __name__ == "__main__":
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



