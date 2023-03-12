import i2CComms

addr = 0x4 # bus address

def sendStart():
    sendByte(0x40)

def sendNum(num, place):
    sendByte(0x80 | (place << 4) | num)

def sendBlank(place):
    sendByte(0x80 | (place << 4) | 15)
    
def sendBrightness(level):
    sendByte(0x60 | level)

def sendPoint(place):
    sendByte(0x50 | place)

def sendEnd():
    sendByte(0x20)

def sendNoop():
    sendByte(0x30)

def sendCommaL(place):
    sendByte(0xE0 | place)

def sendCommaR(place):
    sendByte(0xF0 | place)

def sendOff():
    sendByte(0x10)

def sendOn():
    sendByte(0x11)

def sendIntroOn():
    sendByte(0x12)

def sendByte(sendByte, cnt = 0):
    i2CComms.sendByte(addr, sendByte, cnt)



