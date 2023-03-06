from smbus import SMBus

addr = 0x4 # bus address
bus = SMBus(0) # indicates /dev/ic2-0

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

def sendByte(send_byte, cnt = 0):
    try:
        #print('sendin '+bin(send_byte))
        bus.write_byte(addr, send_byte)
    except:
        print('snd fail no ' + str(cnt + 1))
        if (cnt < 10):
            sendByte(send_byte, cnt + 1)


