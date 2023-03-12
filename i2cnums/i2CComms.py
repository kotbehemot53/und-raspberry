from smbus import SMBus

bus = SMBus(0) # indicates /dev/ic2-0
def sendByte(addr, sendByte, cnt = 0):
    try:
        #print('sendin '+bin(send_byte))
        bus.write_byte(addr, sendByte)
    except:
        print('snd fail no ' + str(cnt + 1))
        if (cnt < 10):
            sendByte(sendByte, cnt + 1)
