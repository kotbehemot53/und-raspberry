import sys
import time
import random
import math
import piToNixie

i = 0
up = False
j = 15
while(1):
    bgn = time.time()

    if (i > 9999):
        i = 0

    # rcv_byte = spi.xfer2([0x40, 0x10 | (math.floor(i / 100) % 10), 0x10 | (math.floor(i/10) % 10), 0x10 | (i % 10), 0x20])

    # piToNixie.sendStart()
    piToNixie.sendNum((math.floor(i / 1000) % 10), 0)
    piToNixie.sendBrightness(j)
    piToNixie.sendNum((math.floor(i / 100) % 10), 1)
    piToNixie.sendBrightness(j)
    piToNixie.sendNum((math.floor(i / 10) % 10), 2)
    piToNixie.sendBrightness(j)
    piToNixie.sendNum((i % 10), 3)
    piToNixie.sendBrightness(j)
    piToNixie.sendPoint(math.floor(i / 10) % 2)
    piToNixie.sendCommaR(2)
    piToNixie.sendEnd()


    if len(sys.argv) <= 1:
        if (i%3 == 0):
            if (up):
                j += 1
            else:
                j -= 1

        if j == 1:
            up = True
        if j == 15:
            up = False

    i += 1

    time.sleep(0.1 - (time.time() - bgn))

