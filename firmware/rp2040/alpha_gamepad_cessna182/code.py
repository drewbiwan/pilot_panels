# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Author: Mark Roberts (mdroberts1243) from Adafruit code
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, miscellaneous stuff and some white text.

"""

# CircuitPython Libraries
import time
import board
import displayio
import terminalio
import digitalio
import analogio
import usb_hid
import struct
from adafruit_hid import find_device

# Local Files
# from hid_pp_generic import pp_gamepad

#######################
# Define functions
#######################
def range_map(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

print("SETTING UP CONFIG")

#######################
# Set up external interfaces
#######################
#i2c = board.I2C()

#######################
# Set up USB HID Gamepad
#######################
gp = find_device(usb_hid.devices, usage_page=0x1, usage=0x05)

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
# Set hardware IO
#######################
# On board GPI
NUM_GPI = 1
gpi = []
gpi.append(digitalio.DigitalInOut(board.GP0))
gpi[0].direction = digitalio.Direction.INPUT
gpi[0].pull = digitalio.Pull.UP
gpi.append(digitalio.DigitalInOut(board.GP1))
gpi[1].direction = digitalio.Direction.INPUT
gpi[1].pull = digitalio.Pull.UP
gpi.append(digitalio.DigitalInOut(board.GP2))
gpi[2].direction = digitalio.Direction.INPUT
gpi[2].pull = digitalio.Pull.UP
gpi.append(digitalio.DigitalInOut(board.GP3))
gpi[3].direction = digitalio.Direction.INPUT
gpi[3].pull = digitalio.Pull.UP
gpi.append(digitalio.DigitalInOut(board.GP22)) #onboard reset
gpi[4].direction = digitalio.Direction.INPUT
gpi[4].pull = digitalio.Pull.UP

# On board ADCs
NUM_ANALOG = 1
analog_values = []
adc = []
adc.append(analogio.AnalogIn(board.A0)) #0
adc.append(analogio.AnalogIn(board.A1)) #1
adc.append(analogio.AnalogIn(board.A2)) #2
#adc = analogio.AnalogIn(board.A0)

# Debug
counter = 0
counter_str = str(counter)

print("COMPLETE")

time.sleep(1)

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
    button_values.append(gpi[0].value)   #0
    button_values.append(gpi[1].value)   #1
    button_values.append(gpi[2].value)   #2
    button_values.append(gpi[3].value)   #3
    button_values.append(gpi[4].value)   #4
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
    # Don't update too often
    time.sleep(0.1)