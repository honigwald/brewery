import RPi.GPIO as GPIO
import time

FREQ = 50

class Servo: 
    def __init__(self, PIN):
        self.PIN = PIN
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN,GPIO.OUT)
        self.pwm = GPIO.PWM(PIN, FREQ) 
        self.pwm.start(2.5)
        self.angle = 0

    def changeAngle(self, angle):
        convertAngle = {
            0: 2.7,
            22.5: 3.9,
            45: 5.2,
            67.5: 6.4,
            90: 7.6,
            112.5: 9,
            135: 10.25,
            157.5: 11.6,
            180: 12.9,
            #180: 2.7,
            #-0: 12.9,
            #-22.5: 11.6,
            #-45: 10.25,
            #-67.5: 9,
            #-90: 7.6,
            #-112.5: 6.4,
            #-135: 5.2,
            #-157.5: 3.9,
            #-180: 12.9
            #0: 12.9,
            #22.5: 11.6,
            #45: 10.25,
            #67.5: 9,
            #90: 7.6,
            #112.5: 6.4,
            #135: 5.2,
            #157.5: 3.9,
            #180: 2.7
        }
        if self.angle != angle:
            GPIO.output(self.PIN, True)
            self.pwm.ChangeDutyCycle(convertAngle.get(angle))
            self.angle = angle
            print self.angle
            time.sleep(1)
            GPIO.output(self.PIN, False)
        self.pwm.ChangeDutyCycle(0)

    def more(self):
        if self.angle == 180:
            print "more: we're at full power"
            GPIO.output(self.PIN, False)
            self.pwm.ChangeDutyCycle(0)
            time.sleep(1)
        else:
            print self.angle
            print "Next angle is: %s" % (self.angle + 22.5)
            self.changeAngle(self.angle + 22.5)
            GPIO.output(self.PIN, False)
            self.pwm.ChangeDutyCycle(0)
            time.sleep(1)

    def less(self):
        if self.angle > 22.5:
            print self.angle
            print "Next angle is: %s" % (self.angle - 22.5)
            self.changeAngle(self.angle - 22.5)
            GPIO.output(self.PIN, False)
            self.pwm.ChangeDutyCycle(0)
            time.sleep(1)
        else:
            print "less: can't go further"
            print "Next angle is: %s" % (45)
            self.changeAngle(45)
            GPIO.output(self.PIN, False)
            self.pwm.ChangeDutyCycle(0)
            time.sleep(1)

### Testcases
#servo = Servo(17)
#servo.changeAngle(45)
#time.sleep(1)
#servo.changeAngle(90)
#time.sleep(1)
#servo.changeAngle(135)
#time.sleep(1)
#servo.changeAngle(180)
#time.sleep(1)
#servo.changeAngle(0)
