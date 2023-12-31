"""
Exercise on Raspberry Pi Pico/MicroPython
with 320x240 ILI9341 SPI Display
"""
from ili934xnew import ILI9341, color565
from machine import Pin, SPI
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32
import time

SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
SCR_ROT = const(2)
CENTER_Y = int(SCR_WIDTH/2)
CENTER_X = int(SCR_HEIGHT/2)

print(os.uname())
# These const define the GPIO pins (not the pico board pins)

TFT_CLK_PIN = const(6)	   # PICO PIN 9	
TFT_MOSI_PIN = const(7)    # PICO PIN 10
TFT_MISO_PIN = const(4)    # NOT NEEDED (PICO PIN 6)

TFT_CS_PIN = const(13)     # PICO PIN 17
TFT_RST_PIN = const(14)    # PICO PIN 19
TFT_DC_PIN = const(15)     # PICO PIN 20
# Other Pins VCC (ILI934) to VCC on PICO PIN 36 (3.3V OUT) 
# GND (ILI934) to GND on PICO  PICO PIN 38

fonts = [glcdfont,tt14,tt24,tt32]
text = 'Hello Raspberry Pi Pico/ili9341'

print(text)
print("fonts available:")
for f in fonts:
    print(f.__name__)

spi = SPI(
    0,
    baudrate=40000000,
    miso=Pin(TFT_MISO_PIN),
    mosi=Pin(TFT_MOSI_PIN),
    sck=Pin(TFT_CLK_PIN))
print(spi)

display = ILI9341(
    spi,
    cs=Pin(TFT_CS_PIN),
    dc=Pin(TFT_DC_PIN),
    rst=Pin(TFT_RST_PIN),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT)

display.erase()
display.set_pos(0,0)

for ff in fonts:
    display.set_font(ff)
    display.print(text)
    
display.set_font(tt24)
display.set_color(color565(255, 255, 0), color565(150, 150, 150))
display.print("\nThanks:")
display.print("https://github.com/jeffmer/micropython-ili9341")

time.sleep(1)

for i in range(170):
    display.scroll(1)
    time.sleep(0.01)
    
time.sleep(1)
for i in range(170):
    display.scroll(-1)
    time.sleep(0.01)
    
time.sleep(1)
for h in range(SCR_WIDTH):
    if h > SCR_HEIGHT:
        w = SCR_HEIGHT
    else:
        w = h
        
    display.fill_rectangle(0, 0, w, h, color565(0, 0, 255))
    time.sleep(0.01)

time.sleep(0.5)
display.erase()

# Helper function to draw a circle from a given position with a given radius
# This is an implementation of the midpoint circle algorithm,
# see https://en.wikipedia.org/wiki/Midpoint_circle_algorithm#C_example 
# for details
def draw_circle(xpos0, ypos0, rad, col=color565(255, 255, 255)):
    x = rad - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (rad << 1)
    while x >= y:
        display.pixel(xpos0 + x, ypos0 + y, col)
        display.pixel(xpos0 + y, ypos0 + x, col)
        display.pixel(xpos0 - y, ypos0 + x, col)
        display.pixel(xpos0 - x, ypos0 + y, col)
        display.pixel(xpos0 - x, ypos0 - y, col)
        display.pixel(xpos0 - y, ypos0 - x, col)
        display.pixel(xpos0 + y, ypos0 - x, col)
        display.pixel(xpos0 + x, ypos0 - y, col)
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (rad << 1)
    
draw_circle(CENTER_X, CENTER_Y, 120)

display.set_pos(1,10)
display.print("helloraspberrypi.blogspot.com")

for c in range(99):
    draw_circle(CENTER_X, CENTER_Y, c, color565(255, 0, 0))
    
for c in range(98):
    draw_circle(CENTER_X, CENTER_Y, c, color565(0, 255, 0))
    
for c in range(97):
    draw_circle(CENTER_X, CENTER_Y, c, color565(0, 0, 255))

print("- bye-")
