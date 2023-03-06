import piToNixie
import random
import time
import math
import sys

#while(1):
for i in range(int(sys.argv[1]), 0, -1):
    piToNixie.sendNum(math.floor(i/1000) % 10, 0)
    piToNixie.sendNum(math.floor(i/100) % 10, 1)
    piToNixie.sendNum(math.floor(i/10) % 10, 2)
    piToNixie.sendNum(math.floor(i/1) % 10, 3)
    piToNixie.sendEnd()
    time.sleep(1)

piToNixie.sendNum(0, 0)
piToNixie.sendNum(0, 1)
piToNixie.sendNum(0, 2)
piToNixie.sendNum(0, 3)
piToNixie.sendPoint(0)
piToNixie.sendPoint(1)
piToNixie.sendEnd()

