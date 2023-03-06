import piToNixie
import random
import time

while(1):
    piToNixie.sendNum(random.randint(0,9), 0)
    piToNixie.sendNum(random.randint(0,9), 1)
    piToNixie.sendNum(random.randint(0,9), 2)
    piToNixie.sendNum(random.randint(0,9), 3)
    piToNixie.sendEnd()
    time.sleep(0.01)

