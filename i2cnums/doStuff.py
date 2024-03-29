import sys
import time
import piToNixie
import piToVFD
import time
import threading
import random
import datetime

import RPi.GPIO as GPIO

import Encoder
from gpiozero import Button

brightnessEncoder = Encoder.Encoder(27, 22)

btnDn = Button(4)
btnUp = Button(17)

currentBrightness = 15

availableModes = ["time", "count", "intro"]
currentMode = "time"
modeChanged = False
# modeChangedAt = None
modeChangedAt = int(time.time())
vfdDimmed = False
poisonReturn = False


def calculateTime():
    commasR = []

    now = time.localtime()
    newTimestr = time.strftime('%H%M%S', now)
    secstr = time.strftime('%S', now)
    if int(secstr[1]) % 2 == 0:
        commasR = [1, 3]
    points = [int(secstr[1]) % 2]

    return [newTimestr, [], commasR, points]


def calculateCount(initTime):
    # pad number with 'a's which will result as lamps being off
    newStr = str(int(time.time() * 10 - initTime * 10)).rjust(6, 'a')
    # print(newStr)
    return [newStr, [], [], []]


def runIntro():
    piToNixie.sendIntroOn()
    return [None, [], [], []]


def calculateBrightness(previousBrightnessEncoderReading, currentBrightness):
    brightnessEncoderReading = brightnessEncoder.read()
    brightnessChanged = False
    # encoder value changes by 4 on every click; we don't wanna record incomplete clicks
    if (brightnessEncoderReading > previousBrightnessEncoderReading + 3):
        previousBrightnessEncoderReading = brightnessEncoderReading
        brightnessChanged = True
        if (currentBrightness < 15):
            currentBrightness += 1
            print("New brightness: " + str(currentBrightness))
    # encoder value changes by 4 on every click; we don't wanna record incomplete clicks
    if (brightnessEncoderReading < previousBrightnessEncoderReading - 3):
        previousBrightnessEncoderReading = brightnessEncoderReading
        brightnessChanged = True
        if (currentBrightness > 1):
            currentBrightness -= 1
            print("New brightness: " + str(currentBrightness))

    return [brightnessChanged, previousBrightnessEncoderReading, currentBrightness]


def sendDisplayedNumber(displayedNumber, commasL, commasR, points):
    if displayedNumber[0].isdigit():
        piToNixie.sendNum(int(displayedNumber[0]), 0)
        piToNixie.sendBrightness(currentBrightness)

    if displayedNumber[1].isdigit():
        piToNixie.sendNum(int(displayedNumber[1]), 1)
        piToNixie.sendBrightness(currentBrightness)

    if displayedNumber[2].isdigit():
        piToNixie.sendNum(int(displayedNumber[2]), 2)
        piToNixie.sendBrightness(currentBrightness)

    if displayedNumber[3].isdigit():
        piToNixie.sendNum(int(displayedNumber[3]), 3)
        piToNixie.sendBrightness(currentBrightness)

    if displayedNumber[4].isdigit():
        piToNixie.sendNum(int(displayedNumber[4]), 4)
        piToNixie.sendBrightness(currentBrightness)

    if displayedNumber[5].isdigit():
        piToNixie.sendNum(int(displayedNumber[5]), 5)
        piToNixie.sendBrightness(currentBrightness)

    for comma in commasL:
        piToNixie.sendCommaL(comma)

    for comma in commasR:
        piToNixie.sendCommaR(comma)

    for point in points:
        piToNixie.sendPoint(point)

    piToNixie.sendEnd()


def sendModeToVFD(mode):
    global vfdDimmed

    modeBytes = bytes(" " + mode, "ascii")
    for idx, modeByte in enumerate(modeBytes):
        piToVFD.sendChar(modeByte, idx)

    piToVFD.sendBrightness(0xFF, 10)  # TODO: use brightness set for this display; indexes reversed?
    # piToVFD.set # TODO: command needed to break fade-in/out here (set constant mode at max brightness)!
    piToVFD.sendMultiFinish()

    vfdDimmed = False


def dimVFDDigit(which):
    time.sleep(random.random() * 6)
    piToVFD.setFadeOut(0, which)
    piToVFD.sendMultiFinish()


def dimVFD():
    global vfdDimmed
    vfdDimmed = True
    # TODO: multiple fade outs lead to all sorts of artifacts random lit segents - why?
    #       also switching during fade-out leads to immediate fade-out of the new value - FIX IT!
    # for i in range(10):
    #     t = threading.Thread(target=dimVFDDigit, args=[i])
    #     t.start()
    piToVFD.setFadeOut(0, 10)
    piToVFD.sendMultiFinish()


def cycleModeUp():
    print("cycle up")
    cycleMode()


def cycleModeDn():
    print("cycle dn")
    cycleMode(False)


def cycleMode(up=True):
    global currentMode
    global modeChanged
    # global modeChangedAt
    global modeChangedAt
    modeChangedAt = int(time.time())
    currentIdx = availableModes.index(currentMode)
    if (up):
        currentIdx += 1
    else:
        currentIdx -= 1

    if currentIdx >= len(availableModes):
        currentIdx = 0
    elif currentIdx < 0:
        currentIdx = len(availableModes) - 1

    currentMode = availableModes[currentIdx]
    modeChanged = True
    # modeChangedAt = int(time.time())


def poisoningPrevention():
    global currentMode
    global poisonReturn

    preventionInterval = 200  # in seconds
    preventionDuration = 5  # in seconds: roughly 0.2 seconds * 10 digits per minute

    if not poisonReturn:  # start procedure
        if (int(time.time()) % preventionInterval) == 0:
            poisonReturn = currentMode
            currentMode = "intro"
    else:  # end procedure
        if (int(time.time()) % preventionInterval) > preventionDuration:
            currentMode = poisonReturn
            poisonReturn = False


try:
    random.seed(int(time.time()))

    # force internal pullups on the brightness encoder pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    btnUp.when_pressed = cycleModeUp
    btnDn.when_pressed = cycleModeDn

    previousBrightnessEncoderReading = brightnessEncoder.read()

    displayedNumber = None
    commasR = []
    commasL = []
    points = []
    introInProgress = False

    piToVFD.sendIntroOff()  # TODO due to a bug in vfd firmware we must wait a bit for the intro to ACTUALLY go off
    time.sleep(1)
    sendModeToVFD(currentMode)

    while (1):
        bgn = time.time()

        poisoningPrevention()

        if currentMode == "time":
            [newDisplayedNumber, newCommasL, newCommasR, newPoints] = calculateTime()
            introInProgress = False
        elif currentMode == "count":
            [newDisplayedNumber, newCommasL, newCommasR, newPoints] = calculateCount(modeChangedAt)
            introInProgress = False
        elif currentMode == "intro":
            # we wanna run the intro only once
            if not (introInProgress):
                [newDisplayedNumber, newCommasL, newCommasR, newPoints] = runIntro()
                introInProgress = True
        else:
            print("Unsupported mode " + currentMode)

        if (modeChanged):
            modeChanged = False
            sendModeToVFD(currentMode)

        if (not (vfdDimmed) and (modeChangedAt < int(time.time()) - 10)):
            dimVFD()

        [brightnessChanged, previousBrightnessEncoderReading, currentBrightness] = calculateBrightness(
            previousBrightnessEncoderReading, currentBrightness)

        # if number set to none, we don't wanna change the display
        if (newDisplayedNumber == None):
            continue

        # dont send new values to lamps if nothing changed
        if ((
                displayedNumber != None and newDisplayedNumber == displayedNumber and newCommasL == commasL and newCommasR == commasR and newPoints == points) and not (
        brightnessChanged)):
            continue

        displayedNumber = newDisplayedNumber
        commasL = newCommasL
        commasR = newCommasR
        points = newPoints

        sendDisplayedNumber(displayedNumber, commasL, commasR, points)

        # print("Time left: " + str(0.05 - (time.time() - bgn)))
        # do the loop every 50 milliseconds
        sleepTime = 0.05 - (time.time() - bgn)
        time.sleep(sleepTime if sleepTime > 0 else 0)

finally:
    GPIO.cleanup()
