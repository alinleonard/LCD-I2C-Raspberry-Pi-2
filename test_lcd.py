from LCDI2C_backpack import LCDI2C_backpack
import time

lcd = LCDI2C_backpack(0x3f)

lcd.message("Welcome\nhttps://github.com/alinleonard/")
time.sleep(2)
for i in range(0,15):
	lcd.scrollDisplayLeft()
	time.sleep(0.5)

time.sleep(5)
lcd.clear() # we need to clear so it sets cursor back

lcd.lcd_string("New message Line 1",lcd.LCD_LINE_1)


for i in range(0,150):
	lcd.lcd_string("Count:"+str(i),lcd.LCD_LINE_2)
	time.sleep(1)