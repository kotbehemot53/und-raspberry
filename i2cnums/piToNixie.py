from smbus import SMBus

addr = 0x4 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

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

def sendByte(send_byte, cnt = 0):
    try:
        #print('sendin '+bin(send_byte))
        bus.write_byte(addr, send_byte)
    except:
        print('snd fail no ' + str(cnt + 1))
        if (cnt < 10):
            sendByte(send_byte, cnt + 1)