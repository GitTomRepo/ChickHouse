#!/usr/bin/python3

from CLOSE_door import CLOSE_door
from OPEN_door import OPEN_door
from ..chickHouse_web.doorCTRL import doorCTRL

import RPi.GPIO as GPIO
import time

class stepperMotor () :
    # Liste des pins de controle du moteur
    motor_pins = []

    # Ajustement de la fréquence de changement de step
    step_sleep = 0.002

    step_count = 4096 # Nombre de step par révolution
    motor_step_counter = 0 # Nombre de pas accomplis

    # True : sans horaire | False : sans anti-horaire
    direction = False 

    # Séquence d'alimentation
    step_sequence = [[1,0,0,1],
                    [1,0,0,0],
                    [1,1,0,0],
                    [0,1,0,0],
                    [0,1,1,0],
                    [0,0,1,0],
                    [0,0,1,1],
                    [0,0,0,1]]
    
    def __init__(self, in1 = 13, in2 = 15, in3 = 16, in4 = 18) :
        GPIO.setmode(GPIO.BCM)
        self.motor_pins = [in1,in2,in3,in4]
        self.setUp_GPIO()

    def setUp_GPIO (self) :
        for pin in self.motor_pins : # Initialisation des IO
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def rotateDEG (self, angle) :
        numStep = int((4096 * angle)/self.step_count) # Conversion : Angle -> Nombre de pas
        self.rotateSTEP(numStep)

    def rotateSTEP (self, numStep) :
        for i in range(numStep):
            for pin in range(len(self.motor_pins)):
                GPIO.output(self.motor_pins[pin], self.step_sequence[self.motor_step_counter][pin])

                if self.direction==True:
                    self.motor_step_counter = (self.motor_step_counter - 1) % 8
                else :
                    self.motor_step_counter = (self.motor_step_counter + 1) % 8

            time.sleep(self.step_sleep)

stepMotor = stepperMotor()

# GPIO - Photo diode
pinLum = 11
GPIO.setup(pinLum, GPIO.IN)

# Initialisation
refreshRate = 100 # En ms
stateDoor = True # True : ouvert | False : fermé
door = doorCTRL()

OPEN_door()

while True :
    if GPIO.input(pinLum) and not stateDoor :
        OPEN_door(stepMotor)
        door.openDoor()
    elif not GPIO.input(pinLum) and stateDoor :
        CLOSE_door(stepMotor)
        door.closeDoor()

    time.sleep(refreshRate)