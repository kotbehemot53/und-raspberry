import i2CComms

LED_MODE_HEARTBEAT = 0
LED_MODE_WARNING = 1
LED_MODE_SQUARE_HEARTBEAT = 3
LED_MODE_DIM = 100

addr = 0x5 # bus address

def sendOn():
    sendByte(0x11)

def sendOff():
    sendByte(0x10)

def sendIntroOn():
    sendByte(0x12)

def sendIntroOff():
    sendByte(0x13)

def sendMultiFinish():
    sendByte(0x20)

def sendLEDMode(mode):
    # TODO: throw exception on illegal modes
    sendByte(0x30 | mode)

def sendChar(char, place):
    # TODO: throw exception on illegal place
    # TODO: throw exception on illegal char
    sendByte(0x80 | place)
    sendByte(char)

#name's fucked, right?
def sendCustomByte(byte, place):
    # TODO: throw exception on illegal place
    # TODO: throw exception on illegal byte
    sendByte(0x90 | place)
    sendByte(byte)

def sendPointR(place):
    # TODO: throw exception on illegal place
    sendByte(0xF0 | place)

def sendBrightness(duty, place):
    # TODO: throw exception on illegal duty value
    # TODO: throw exception on illegal place
    sendByte(0x60 | place)
    sendByte(duty)

def setFadeIn(targetDuty, place):
    # TODO: throw exception on illegal duty value
    # TODO: throw exception on illegal place
    sendByte(0xA0 | place)
    sendByte(targetDuty)

def setFadeOut(targetDuty, place):
    # TODO: throw exception on illegal duty value
    # TODO: throw exception on illegal place
    sendByte(0xB0 | place)
    sendByte(targetDuty)

def setFadeTime(time, place):
    # TODO: throw exception on illegal time value
    # TODO: throw exception on illegal place
    sendByte(0xC0 | place)
    sendByte(time)

def sendClear():
    sendByte(0xD0)

def sendByte(byteToSend):
    i2CComms.sendByte(addr, byteToSend, 0)
