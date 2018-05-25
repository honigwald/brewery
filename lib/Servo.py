import RPi.GPIO as GPIO
import time         

#PIN = 03
FREQ = 50

class Servo:
	def __init__(self, PIN):
		self.PIN = PIN
		GPIO.setwarnings(False)
		GPIO.setmode (GPIO.BOARD) 
		GPIO.setup(PIN,GPIO.OUT)
		self.pwm = GPIO.PWM(PIN, FREQ) 
		self.pwm.start(0)     

	def changeAngle(self, angle):
		convertAngle = {
			0: 3,
			22.5: 4.1,
			45: 4.9,
			67.5: 5.9,
			90: 6.9,
			112.5: 7.9,
			135: 9,
			157.5: 10.1,
			180: 11.2
		}
		GPIO.output(self.PIN, True)
		self.pwm.ChangeDutyCycle(convertAngle.get(angle))
		time.sleep(1)
		GPIO.output(self.PIN, False)
		self.pwm.start(0)     

### Some Testcases
servo = Servo(03)
servo.changeAngle(0)
#servo.changeAngle(22.5)
#servo.changeAngle(45)
#servo.changeAngle(67.5)
#servo.changeAngle(90)
#servo.changeAngle(112.5)
#servo.changeAngle(135)
#servo.changeAngle(157.5)
servo.changeAngle(180)
servo.changeAngle(0)
