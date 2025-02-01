USE_FAKE_GPIO = True # Chage to FALSE if testing in the Raspberry Pi

if USE_FAKE_GPIO:
    from .fake_gpio import GPIO  # For running app
else:
    import RPi.GPIO as GPIO  # For testing in Raspberry Pi


# import ...
import time
import random
class SensorController:

    def _init_(self):
        self.PIN_TRIGGER = 18  # do not change
        self.PIN_ECHO = 24  # do not change
        self.distance = 0
        self.color_from_distance = [False, False, False]
        print('Sensor controller initiated')

    def track_rod(self):
        if not USE_FAKE_GPIO:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.PIN_TRIGGER,GPIO.OUT)
            GPIO.setup(self.PIN_ECHO,GPIO.IN)
            GPIO.output( self.PIN_TRIGGER, False)
        #time.sleep(2)
            self.distance = 0
            for i in range(10):
                distance = 0
                GPIO.output( self.PIN_TRIGGER, True)
                time.sleep(0.00001)
                GPIO.output( self.PIN_TRIGGER, False)
                pulse_start = 0
                pulse_end = 0
                while GPIO.input(self.PIN_ECHO)==0:
                    pulse_start = time.time()
                while GPIO.input(self.PIN_ECHO)==1:
                    pulse_end = time.time()
                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150
                distance = round(distance, 2)
                self.distance+=distance
            self.distance/=10
        else:
            self.distance = random.randint(4,21)
        if(self.distance >= 16 and self.distance <= 21):
            print("8")
            self.color_from_distance=[True, False, False]
        elif(self.distance >= 10 and self.distance <= 15):
            print("3")
            self.color_from_distance=[False, True, False]
        elif(self.distance >= 4 and self.distance <= 9):
            print("1")
            self.color_from_distance=[False, False, True]
        else:
            print('else condition')
        print('Monitoring',self.distance)

    def get_distance(self):
        return self.distance

    def get_shape_from_distance(self):
        return self.color_from_distance
