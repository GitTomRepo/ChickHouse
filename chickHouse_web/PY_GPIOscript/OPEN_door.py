#!/usr/bin/python3

from mainAuto_door import stepperMotor
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

# GPIO - Fin de course
endUp = 36
GPIO.setup(endUp, GPIO.IN)

def OPEN_door (stepMotor = stepperMotor(), refreshRate = 10) :
    while not GPIO.input(endUp) :
        stepMotor.direction = True
        stepMotor.rotateSTEP(4)
        sleep(refreshRate)