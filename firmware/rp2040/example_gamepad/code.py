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

import usb_hid
from hid_gamepad import Gamepad

# can try import bitmap_label below for alternative
from adafruit_display_text import label
import adafruit_displayio_sh1107

def range_map(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

displayio.release_displays()
# oled_reset = board.D9

# Use for I2C
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64
BORDER = 2

# Terminal parameters
DISP_LINES = 6
DISP_OFFSET = 4
DISP_SPACING = 10

display = adafruit_displayio_sh1107.SH1107(
    display_bus, width=WIDTH, height=HEIGHT, rotation=0, auto_refresh=True
)

# Make the display context
#splash = displayio.Group()
#display.show(splash)
#display.refresh(minimum_frames_per_second=10)

# Set up USB HID Gamepad
gp = Gamepad(usb_hid.devices)

# Set up IO
pb_a = digitalio.DigitalInOut(board.D9)
pb_a.direction = digitalio.Direction.INPUT
pb_a.pull = digitalio.Pull.UP

pb_b = digitalio.DigitalInOut(board.D6)
pb_b.direction = digitalio.Direction.INPUT
pb_b.pull = digitalio.Pull.UP

pb_c = digitalio.DigitalInOut(board.D5)
pb_c.direction = digitalio.Direction.INPUT
pb_c.pull = digitalio.Pull.UP

ts_a = digitalio.DigitalInOut(board.D10)
ts_a.direction = digitalio.Direction.INPUT
ts_a.pull = digitalio.Pull.UP

pot_a = analogio.AnalogIn(board.A0)

led_a = 1
led_b = 1
led_c = 1

counter = 0
counter_str = str(counter)

"""
# Draw some label text
text1 = "Panel Helloworld"  # overly long to see where it clips
text_area1 = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, x=4, y=DISP_OFFSET+DISP_SPACING*0)
splash.append(text_area1)
text2 = "Drew Coker"
text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF, x=4, y=DISP_OFFSET+DISP_SPACING*1)
splash.append(text_area2)
text3 = ""
text_area3 = label.Label(terminalio.FONT, text=text3, color=0xFFFFFF, x=4, y=DISP_OFFSET+DISP_SPACING*2)
splash.append(text_area3)
text4 = ""
text_area4 = label.Label(terminalio.FONT, text=text4, color=0xFFFFFF, x=4, y=DISP_OFFSET+DISP_SPACING*3)
splash.append(text_area4)
text5 = ""
text_area5 = label.Label(terminalio.FONT, text=text5, color=0xFFFFFF, x=4, y=DISP_OFFSET+DISP_SPACING*4)
splash.append(text_area5)
text6 = ""
text_area6 = label.Label(terminalio.FONT, text=text6, color=0xFFFFFF, x=4, y=DISP_OFFSET+DISP_SPACING*5)
splash.append(text_area6)
"""
time.sleep(1)

while True:
    #update IO, strings
    counter = counter + 1
    counter_str = str(counter)

    led_a = 1
    led_b = 1
    led_c = 1

    # Update strings for display
    pb_a_str = str(int(pb_a.value))
    pb_b_str = str(int(pb_b.value))
    pb_c_str = str(int(pb_c.value))
    ts_a_str = str(int(ts_a.value))
    pot_a_str = str(pot_a.value)
    led_a_str = str(led_a)
    led_b_str = str(led_b)
    led_c_str = str(led_c)

    # Update connection
    HID_str = "DEADBEEF"

    # Debug
    print(pb_a_str + " " + pb_b_str + " " + pb_c_str + " " + ts_a_str + " " + pot_a_str)

    # Update display layers
    """
    text_area1.text = "Panel Debug"
    text_area2.text = "PBS A: " + pb_a_str + ", B: " + pb_b_str + " C: " + pb_c_str
    text_area3.text = "LED A: " + led_a_str + ", B: " + led_b_str + " C: " + led_c_str
    text_area4.text = "TS A: " + ts_a_str + ", POT A: " + pot_a_str
    text_area5.text = "HID:" + HID_str
    text_area6.text = "COUNTER: " + counter_str
    """
    gp.move_joysticks(x=range_map(pot_a.value,0,65535,-127,127))

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

    #display.refresh()

    # Don't update too often
    time.sleep(0.01)