from smbus import SMBus
import time

bus = SMBus(0) # indicates /dev/ic2-0
def sendByte(addr, byteToSend, cnt = 0):
    try:
        #print('sendin '+bin(send_byte))
        bus.write_byte(addr, byteToSend)
        time.sleep(0.01) # maybe this will ensure that the receiver can handle all messages
    except:
        print('snd fail no ' + str(cnt + 1))
        if (cnt < 10):
            sendByte(addr, byteToSend, cnt + 1)
