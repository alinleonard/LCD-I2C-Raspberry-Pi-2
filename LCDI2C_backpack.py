#!/usr/bin/python
#--------------------------------------
#  lcd_i2c.py
#  LCD test script using I2C backpack.
#  Supports 16x2 and 20x4 screens.
#
#--------------------------------------
import smbus
import time


class LCDI2C_backpack(object):
  # Define some device parameters
  I2C_ADDR  = 0x3f # I2C device address
  LCD_WIDTH = 16   # Maximum characters per line

  # Define some device constants
  LCD_CHR = 1 # Mode - Sending command
  LCD_CMD = 0 # Mode - Sending data

  LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
  LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
  LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
  LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

  LCD_BACKLIGHT  = 0x08  # On
  #LCD_BACKLIGHT = 0x00  # Off

  ENABLE = 0b00000100 # Enable bit

  # Timing constants
  E_PULSE = 0.0005
  E_DELAY = 0.0005

  #Open I2C interface
  #bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
  bus = smbus.SMBus(1) # Rev 2 Pi uses 1

  LCD_CURSORSHIFT = 0x10
  LCD_DISPLAYMOVE = 0x08
  LCD_MOVERIGHT = 0x04
  LCD_MOVELEFT = 0x00

  LCD_ENTRYSHIFTINCREMENT = 0x01
  LCD_ENTRYMODESET = 0x04

  def __init__(self, I2C_ADDR):
    self.I2C_ADDR = I2C_ADDR;
    self.init()
    self.clear()

  def init(self):
    # Initialise display
    self.lcd_byte(0x33,self.LCD_CMD) # 110011 Initialise
    self.lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise
    self.lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction
    self.lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
    self.lcd_byte(0x28,self.LCD_CMD) # 101000 Data length, number of lines, font size
    self.lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display
    time.sleep(self.E_DELAY)

  def lcd_byte(self, bits, mode):
    # Send byte to data pins
    # bits = the data
    # mode = 1 for character
    #        0 for command

    self.bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
    self.bits_low = mode | ((bits<<4) & 0xF0) | self.LCD_BACKLIGHT

    # High bits
    self.bus.write_byte(self.I2C_ADDR, self.bits_high)
    self.lcd_toggle_enable(self.bits_high)

    # Low bits
    self.bus.write_byte(self.I2C_ADDR, self.bits_low)
    self.lcd_toggle_enable(self.bits_low)

  def lcd_toggle_enable(self, bits):
    # Toggle enable
    time.sleep(self.E_DELAY)
    self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
    time.sleep(self.E_PULSE)
    self.bus.write_byte(self.I2C_ADDR,(bits & ~self.ENABLE))
    time.sleep(self.E_DELAY)

  def scrollDisplayRight(self):
    self.lcd_byte(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT, self.LCD_CMD)
  
  def scrollDisplayLeft(self):
    self.lcd_byte(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT, self.LCD_CMD)

  def message(self, text):
    # Send string to display
    for char in text:
            if char == '\n':
                self.lcd_byte(0xC0, self.LCD_CMD)  # next line
            else:
                self.lcd_byte(ord(char), self.LCD_CHR)

  def lcd_string(self, message,line):
    # Send string to display
    message = message.ljust(self.LCD_WIDTH," ")
    self.lcd_byte(line, self.LCD_CMD)

    for i in range(self.LCD_WIDTH):
      self.lcd_byte(ord(message[i]),self.LCD_CHR)


  def clear(self):
    self.lcd_byte(0x01, self.LCD_CMD)

