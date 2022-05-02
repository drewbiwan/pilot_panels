"""
File: code.py
Description: Custom HID gamepad
Author: Drew Coker
Date: March 2022

"""

# CircuitPython Libraries
import time
import board
import busio
import digitalio
import analogio
import usb_hid
import struct
from adafruit_hid import find_device
import asyncio as uasyncio

# Local Files
# from hid_pp_generic import pp_gamepad

#######################
# Define Parameters
#######################
BUILD_STR = "Generic Gamepad"

logical_update_ms = 10 #update rate for logical io
analog_update_ms = 50 #update rate for analog io
serial_update_ms = 100 #time between serial parse updates

#######################
# Define Classes #TODO: MOVE TO ANOTHER FILES
#######################
class leds:
    def __init__(self,pin):
        self.pin = pin

class gpi_pins_c:
    def __init__(self):
        self.pins = []
        self.strings = []
        self.len = 0
        self.values = []
        self.values_old = []

    def add(self,pin,string):
        self.pins.append(pin)
        self.strings.append(string)
        self.len = len(self.pins)
        self.values.append(False)
        self.values_old.append(False)
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP

    def get_string(self,ind):
        return self.strings[ind]

    def get_value(self,ind):
        return self.values[ind]

    def update_values(self):
        self.values_old = self.values
        for ind in range(self.len):
            pin = self.pins[ind]
            self.values[ind] = pin.value

    def print_values(self):
        print("GPI Values:")
        for ind in range(self.len):
            print("\t" + self.strings[ind] + "\t=" + str(self.values[ind]))


#######################
# Define functions
#######################
# re-range for adc inputs
def range_map(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Status LED loop
async def blink(led,period_ms): 
    while True:
        led.value = True
        await uasyncio.sleep_ms(period_ms)
        led.value = False
        await uasyncio.sleep_ms(period_ms)

async def print_status(gpi_pins,period_ms): 
    while True:
        gpi_pins.print_values()
        await uasyncio.sleep_ms(period_ms)

async def update_digital_report(gpi_pins,usb_device,period_ms): 
    button_hid_report = bytearray(4)
    while True:
        button_hid_report_last = button_hid_report
        gpi_pins.update_values()
        button_hid_report = pack_report(button_hid_report,gpi_pins)
        usb_device.send_report(button_hid_report,1)
        await uasyncio.sleep_ms(period_ms)

async def main_loop(usb_gp,gpi_pins,led_pins):
    digital_task = uasyncio.create_task(update_digital_report(usb_gp,gpi_pins,10))
    blink_task = uasyncio.create_task(blink(led_pins,500))
    print_task = uasyncio.create_task(print_status(gpi_pins,1000))
    await uasyncio.gather(digital_task,blink_task,print_task)



#######################
# Power up configuration
#######################

print("--------------------")
print("Power up configuration")
print("--------------------")

#######################
# Set up USB HID Gamepad
#######################
usb_gp = find_device(usb_hid.devices, usage_page=0x1, usage=0x05)

#######################
# Raw IO to HID
#######################
button_hid_report = bytearray(4)
button_hid_report_last = bytearray(4)

analog_hid_report = bytearray(8)
analog_hid_report_last = bytearray(8)

NUM_BUTTOMS = 32
button_values = []

NUM_AXES = 6
axis_values = []

#######################
# Set up External Serial Interfaces
#######################
i2c0 = busio.I2C(board.GP21,board.GP20) #on board ADC on this bus
# i2c1 = busio.I2C(board.GP19,board.GP18) #qwiic connector

#######################
# Set up Digital Inputs
#######################
gpi_pins = gpi_pins_c()
gpi_pins.add(digitalio.DigitalInOut(board.GP0),'GP0')
gpi_pins.add(digitalio.DigitalInOut(board.GP1),'GP1')
gpi_pins.add(digitalio.DigitalInOut(board.GP2),'GP2')
gpi_pins.add(digitalio.DigitalInOut(board.GP3),'GP3')
gpi_pins.add(digitalio.DigitalInOut(board.GP4),'GP4')
gpi_pins.add(digitalio.DigitalInOut(board.GP5),'GP5')
gpi_pins.add(digitalio.DigitalInOut(board.GP6),'GP6')
gpi_pins.add(digitalio.DigitalInOut(board.GP7),'GP7')
gpi_pins.add(digitalio.DigitalInOut(board.GP8),'GP8')
gpi_pins.add(digitalio.DigitalInOut(board.GP9),'GP9')
gpi_pins.add(digitalio.DigitalInOut(board.GP10),'GP10')
gpi_pins.add(digitalio.DigitalInOut(board.GP11),'GP11')
gpi_pins.add(digitalio.DigitalInOut(board.GP12),'GP12')
gpi_pins.add(digitalio.DigitalInOut(board.GP13),'GP13')
gpi_pins.add(digitalio.DigitalInOut(board.GP14),'GP14')
gpi_pins.add(digitalio.DigitalInOut(board.GP15),'GP15')
gpi_pins.add(digitalio.DigitalInOut(board.GP22),'ONBRD PB')

gpi_pins.update_values()

#######################
# Set up Analog Inputs
#######################
NUM_ANALOG = 1
analog_values = []
adc = []
adc_string = []
adc.append(analogio.AnalogIn(board.A0)) #0
adc_string.append('PICO A0: PLACEHOLDER')
adc.append(analogio.AnalogIn(board.A1)) #1
adc_string.append('PICO A1: PLACEHOLDER')
adc.append(analogio.AnalogIn(board.A2)) #2
adc_string.append('PICO A2: PLACEHOLDER')
#adc = analogio.AnalogIn(board.A0)

#######################
# Set up Digital Outputs
#######################
blinky_led = digitalio.DigitalInOut(board.LED)
blinky_led.direction = digitalio.Direction.OUTPUT
blinky_led.value = True

#######################
# Set up Debug
#######################
counter = 0
counter_str = str(counter)

#######################
# Report Status
#######################
print("--------------------")
print("Hardware Report")
print("--------------------")
gpi_pins.print_values()

print("ADC Mapping:")
for ii in range(len(adc)):
    print("\t" + adc_string[ii])

#######################
# Start Async loop
#######################
print("--------------------")
print("Entering ASYNC Loop")
print("--------------------")

while (True):
    uasyncio.run(main_loop(usb_gp,gpi_pins,blinky_led,1))
    

print("--------------------")
print("Program Exiting...")
print("--------------------")

""" 
print("--------------------")
print("Entering HID mode")
print("--------------------")

while True:
    now = time.monotonic()
    #update IO, strings
    counter = counter + 1
    counter_str = str(counter)
    
    # Map Values to HID 
    axis_values = []
    axis_values.append(range_map(adc[0].value,0,65535,-127,127))    #x
    axis_values.append(range_map(adc[1].value,0,65535,-127,127))    #y
    axis_values.append(range_map(adc[2].value,0,65535,-127,127))    #z
    axis_values.append(range_map(adc[2].value,0,65535,-127,127))    #rotx
    axis_values.append(range_map(adc[2].value,0,65535,-127,127))    #roty
    axis_values.append(range_map(adc[2].value,0,65535,-127,127))    #rotz
    axis_values.append(range_map(adc[2].value,0,65535,-127,127))    #slider
    axis_values.append(range_map(adc[2].value,0,65535,-127,127))    #slider

    button_values = []
    button_values.append(not gpi[0].value)   #0
    button_values.append(not gpi[1].value)   #1
    button_values.append(not gpi[2].value)   #2
    button_values.append(not gpi[3].value)   #3
    button_values.append(not gpi[4].value)   #4
    button_values.append(False)          #5
    button_values.append(False)          #6
    button_values.append(False)          #7
    button_values.append(False)          #8
    button_values.append(False)          #9
    button_values.append(False)          #10
    button_values.append(False)          #11
    button_values.append(False)          #12
    button_values.append(False)          #13
    button_values.append(False)          #14
    button_values.append(False)          #15

    button_values.append(False)          #16
    button_values.append(False)          #17
    button_values.append(False)          #18
    button_values.append(False)          #19
    button_values.append(False)          #20
    button_values.append(False)          #21
    button_values.append(False)          #22
    button_values.append(False)          #23
    button_values.append(False)          #24
    button_values.append(False)          #25
    button_values.append(False)          #26
    button_values.append(False)          #27
    button_values.append(False)          #28
    button_values.append(False)          #29
    button_values.append(False)          #30
    button_values.append(False)          #31

    # Map HID to raw words
    button_hid_words = []
    word = 0
    for kk in range (0,2):
        word = 0
        for ii in range(0,16): #16 buttons per word
            word = word | (button_values[ii+kk*16] << ii)
        button_hid_words.append(word)
        #print(word)


    struct.pack_into(
        "<HH",
        button_hid_report,
        0,
        button_hid_words[0],
        button_hid_words[1]
    )
    struct.pack_into(
        "<bbbbbbbb",
        analog_hid_report,
        0,
        axis_values[0],
        axis_values[1],
        axis_values[2],
        axis_values[3],
        axis_values[4],
        axis_values[5],
        axis_values[6],
        axis_values[7]
    )

    #send report
    #print(button_hid_report)
    #print(analog_hid_report)
    gp.send_report(button_hid_report,1)
    gp.send_report(analog_hid_report,2)

    #print(time.monotonic()-now)
"""

"""
if True | (hid_report_last != hid_report):
    print(hid_report)
    gp.send_report(hid_report)
    hid_report_last = hid_report
    """

# Use Class to send report
"""
gp.move_joysticks(axis_values[0],axis_values[1],axis_values[2],axis_values[3],axis_values[4],axis_values[5])
for ii,  button_value in enumerate(button_values):
    if button_value:
        #print("BUTTON PRESS: {}".format(ii))
        gp.press_buttons(ii+1) #zero indexing is better
    else:
        gp.release_buttons(ii+1)
"""

"""
# Don't update too often
time.sleep(0.1) 
"""
