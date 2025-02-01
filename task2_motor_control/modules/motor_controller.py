USE_FAKE_GPIO = True # Chage to FALSE if testing in the Raspberry Pi
import random

if USE_FAKE_GPIO:
    from .fake_gpio import GPIO  # For running app
else:
    import RPi.GPIO as GPIO  # For testing in Raspberry Pi
from time import sleep

class MotorController(object):

    def __init__(self):
        self.working = False

    def start_motor(self):
        self.PIN_STEP = 25  # do not change
        self.PIN_DIR = 8  # do not change
        self.CW = 0 # clockwise rotation
        self.CCW = 1 # counterclockwise rotation
        self.SPR = 1600 # steps per revolution
        direction=[self.CW,self.CCW]
        random_direction = random.choice(direction)
        rotate_direction="Counter clockwise"
        if(random_direction==0):
            rotate_direction="Clockwise"
        GPIO.setmode(GPIO.BCM)
        if not USE_FAKE_GPIO:
            GPIO.setwarnings(False)
        GPIO.setup(self.PIN_STEP, GPIO.OUT)
        GPIO.setup(self.PIN_DIR, GPIO.OUT)
        GPIO.output(self.PIN_DIR, random_direction)
        print("Motor is start")
        #GPIO.setup(self.PIN_STEP, GPIO.OUT)
        #GPIO.setup(self.PIN_DIR, GPIO.OUT)
        #GPIO.output(self.PIN_DIR, self.CW)
        first_step_Count = 20
        second_step_count = 120
        last_step_Count = 40
        delay = 0.037 # 1600/60=f, t=1/f
        angle=[800,1600]
        random_num = random.choice(angle)
        angle_rotate=360
        if(random_num==800):
            angle_rotate=180

        self.working = True
        for x in range(random_num):
            if(self.working == True):
                print("Motor is Runing")
                
                GPIO.output(self.PIN_STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(self.PIN_STEP, GPIO.LOW)
        print("Motor Rotated ",angle_rotate," degree ",rotate_direction)

        self.working = False

    def stop_motor(self):
        #GPIO.cleanup()
        self.working = False
    def is_working(self):

        return self.working
