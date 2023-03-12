from smbus import SMBus

addr = 0x5 # bus address
bus = SMBus(0) # indicates /dev/ic2-0

def sendOff():
    sendByte(0x10)
