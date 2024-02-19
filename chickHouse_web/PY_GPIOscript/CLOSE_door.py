#!/usr/bin/python3

from mainAuto_door import stepperMotor
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

# GPIO - Fin de course
endDown = 37
GPIO.setup(endDown, GPIO.IN)

def CLOSE_door (stepMotor = stepperMotor(), refreshRate = 10) :
    while not GPIO.input(endDown) :
        stepMotor.direction = False
        stepMotor.rotateSTEP(4)
        sleep(refreshRate)