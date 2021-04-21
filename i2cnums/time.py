import sys
import time
import piToNixie
import datetime

while(1):
    bgn = time.time()

    now = time.localtime()
    if len(sys.argv) > 1:
        timestr = time.strftime('%H%M', now)
    else:
        timestr = time.strftime('%M%S', now)

    secstr = time.strftime('%S', now)

    piToNixie.sendNum(int(timestr[0]), 0)
    piToNixie.sendNum(int(timestr[1]), 1)
    piToNixie.sendNum(int(timestr[2]), 2)
    piToNixie.sendNum(int(timestr[3]), 3)
    piToNixie.sendPoint(int(secstr[1]) % 2)
    
    piToNixie.sendEnd()
    
    time.sleep(0.05 - (time.time() - bgn))
