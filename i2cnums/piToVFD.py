from smbus import SMBus

addr = 0x5 # bus address
bus = SMBus(0) # indicates /dev/ic2-0

def sendOff():
    sendByte(0x10)

def sendByte(send_byte, cnt = 0):
    try:
        #print('sendin '+bin(send_byte))
        bus.write_byte(addr, send_byte)
    except:
        print('snd fail no ' + str(cnt + 1))
        if (cnt < 10):
            sendByte(send_byte, cnt + 1)