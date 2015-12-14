from LCDI2C_backpack import LCDI2C_backpack

i = 5

lcd = LCDI2C_backpack(0x3f)
lcd.message("Working\nCount:" + str(i))
