# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Author: Mark Roberts (mdroberts1243) from Adafruit code
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, miscellaneous stuff and some white text.

"""

import time
import board
import displayio
import terminalio
import digitalio
import analogio
import adafruit_matrixkeypad
from adafruit_seesaw import seesaw, rotaryio
from adafruit_seesaw import digitalio as seesaw_digitalio

import usb_hid
from hid_gamepad import Gamepad

#######################
# Define functions
#######################
def range_map(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

print("SETTING UP CONFIG")

#######################
# Set up external interfaces
#######################
i2c = board.I2C()

#######################
# Set up USB HID Gamepad
#######################
gp = Gamepad(usb_hid.devices)

#######################
# Raw IO to HID
#######################
NUM_BUTTOMS = 16
button_values = []

NUM_AXES = 4
axis_values = []

#######################
# Set hardware IO
#######################
# On board GPI
NUM_GPI = 1
gpi = []
gpi.append(digitalio.DigitalInOut(board.D4))
gpi[0].direction = digitalio.Direction.INPUT
gpi[0].pull = digitalio.Pull.UP

# On board ADCs
NUM_ANALOG = 1
analog_values = []
adc = []
adc.append(analogio.AnalogIn(board.A0)) #0
#adc = analogio.AnalogIn(board.A0)

# Key matrix
# C2 R1 C1 R4  C3  R3  R2
# D5 D6 D9 D10 D11 D12 D13
cols = [digitalio.DigitalInOut(x) for x in (board.D9, board.D5, board.D11)]
rows = [digitalio.DigitalInOut(x) for x in (board.D6, board.D13, board.D12, board.D10)]
keys = ((1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        ('*', 0, '#'))
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

# Rotary encoder stemma
seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)
seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
seesaw_button = seesaw_digitalio.DigitalIO(seesaw, 24)

encoder = rotaryio.IncrementalEncoder(seesaw)
new_position = -encoder.position

# Debug
counter = 0
counter_str = str(counter)

print("COMPLETE")

time.sleep(1)

while True:
    #update IO, strings
    counter = counter + 1
    counter_str = str(counter)

    keys = keypad.pressed_keys
    
    old_position = new_position
    new_position = -encoder.position
    if new_position > old_position:
        encoder_incr = True
        encoder_decr = False
    elif new_position < old_position:
        encoder_incr = False
        encoder_decr = True
    else:
        encoder_incr = False
        encoder_decr = False
    
    #range_map(analog[0].value,0,65535,-127,127)
    axis_values = []
    axis_values.append(range_map(adc[0].value,0,65535,-127,127))
    axis_values.append(range_map(adc[0].value,0,65535,-127,127))
    axis_values.append(range_map(adc[0].value,0,65535,-127,127))
    axis_values.append(range_map(adc[0].value,0,65535,-127,127))

    button_values = []
    button_values.append(0 in keys)             #0
    button_values.append(1 in keys)             #1
    button_values.append(2 in keys)             #2
    button_values.append(3 in keys)             #3
    button_values.append(4 in keys)             #4
    button_values.append(5 in keys)             #5
    button_values.append(6 in keys)             #6
    button_values.append(7 in keys)             #7
    button_values.append(8 in keys)             #8
    button_values.append(9 in keys)             #9
    button_values.append("*" in keys)           #10
    button_values.append("#" in keys)           #11
    button_values.append(gpi[0].value)          #12, Toggle switch
    button_values.append(not seesaw_button.value)   #13, i2c rotary push button
    button_values.append(encoder_incr)          #14
    button_values.append(encoder_decr)          #15

    # Update connection
    HID_str = "DEADBEEF"

    # Debug
    #print("Buttons: {}".format(button_values[0].value))
    #print("Analog: {}".format(axis_values[0]))

    gp.move_joysticks(axis_values[0],axis_values[1],axis_values[2],axis_values[3])

    for ii,  button_value in enumerate(button_values):
        if button_value:
            print("BUTTON PRESS: {}".format(ii))
            gp.press_buttons(ii+1) #zero indexing is better
        else:
            gp.press_buttons(ii+1)

    """
    if pb_a.value:
        gp.release_buttons(1)
    else:
        gp.press_buttons(1)

    if pb_b.value:
        gp.release_buttons(2)
    else:
        gp.press_buttons(2)

    if pb_c.value:
        gp.release_buttons(3)
    else:
        gp.press_buttons(3)

    if ts_a.value:
        gp.release_buttons(4)
    else:
        gp.press_buttons(4)
    """
    # Don't update too often
    time.sleep(0.1)