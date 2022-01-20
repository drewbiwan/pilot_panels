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

# can try import bitmap_label below for alternative
from adafruit_display_text import label
import adafruit_displayio_sh1107

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
    display_bus, width=WIDTH, height=HEIGHT, rotation=0
)

# Make the display context
splash = displayio.Group()
display.show(splash)

# Set up IO
pb_a = 0
pb_b = 0
pb_c = 0

ts_a = 0

pot_a = 50

led_a = 1
led_b = 1
led_c = 1

# Set up Strings for debug
pb_a_str = str(pb_a)
pb_b_str = str(pb_b)
pb_c_str = str(pb_c)

ts_a_str = str(ts_a)

pot_a_str = str(pot_a)

led_a_str = str(led_a)
led_b_str = str(led_b)
led_c_str = str(led_c)

HID_str = "not connected"

counter = 0
counter_str = str(counter)


# Draw some label text
text1 = "Panel Helloworld"  # overly long to see where it clips
text_area1 = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, x=4, y=DISP_OFFSET+DISP_SPACING*0)
splash.append(text_area1)
text2 = "PBS A: " + pb_a_str + ", B: " + pb_b_str + " C: " + pb_c_str
text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF, x=4, y=DISP_OFFSET+DISP_SPACING*1)
splash.append(text_area2)
text3 = "LED A: " + led_a_str + ", B: " + led_b_str + " C: " + led_c_str
text_area3 = label.Label(terminalio.FONT, text=text3, color=0xFFFFFF, x=4, y=DISP_OFFSET+DISP_SPACING*2)
splash.append(text_area3)
text4 = "TS A: " + ts_a_str + ", POT A: " + pot_a_str
text_area4 = label.Label(terminalio.FONT, text=text4, color=0xFFFFFF, x=4, y=DISP_OFFSET+DISP_SPACING*3)
splash.append(text_area4)
text5 = "HID:" + HID_str
text_area5 = label.Label(terminalio.FONT, text=text5, color=0xFFFFFF, x=4, y=DISP_OFFSET+DISP_SPACING*4)
splash.append(text_area5)
text6 = "COUNTER: " + counter_str
text_area6 = label.Label(terminalio.FONT, text=text6, color=0xFFFFFF, x=4, y=DISP_OFFSET+DISP_SPACING*5)
splash.append(text_area6)

while True:
    #update IO
    counter = counter + 1
    counter_str = str(counter)

    

    #update display
    text1 = "Panel Helloworld"  # overly long to see where it clips
    text2 = "PBS A: " + pb_a_str + ", B: " + pb_b_str + " C: " + pb_c_str
    text3 = "LED A: " + led_a_str + ", B: " + led_b_str + " C: " + led_c_str
    text4 = "TS A: " + ts_a_str + ", POT A: " + pot_a_str
    text5 = "HID:" + HID_str
    text_area6.text = "COUNTER: " + counter_str

    #display.refresh()

    # Don't update too often
    time.sleep(0.1)