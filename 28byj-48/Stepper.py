import RPi.GPIO as GPIO
from time import sleep

'''
* THIS CODE IS FOR CONTROLLING STEPPER ENGINE 28byj-48
* TO INTANTIATE THE STEPPER YOU'VE TO DECLARE WHICH GPIO
  PINS ARE USED FOR THE 4 INPUT PINS
'''
### SOME CONSTANTS
TIME = 0.003		# TIME needed for engine to reach estimated position
ONEHALFSTEP = 2.56	# step width for one step on a half circle
ONEFULLSTEP = 5.12	# step width for one step on a full circle


class Stepper:
	def __init__(self, pins):
		self.pins = pins
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		for pin in pins:
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, False)
		self.percent = 0

	# MOVES THE STEPPER <n> STEPS TO THE RIGHT
	def left(self, n):
		for i in range(n):
			self.step1()
			self.step2()
			self.step3()
			self.step4()
			self.step5()
			self.step6()
			self.step7()
			self.step8()
	
	# MOVES THE STEPPER <n> STEPS TO THE LEFT
	def right(self, n):
		for i in range(n):
			self.step8()
			self.step7()
			self.step6()
			self.step5()
			self.step4()
			self.step3()
			self.step2()
			self.step1()

	def halfcircle(self, percent):
		if self.percent > percent:
			# go left
			n = ONEHALFSTEP * abs(percent - self.percent)
			print n
			self.percent = percent
			self.left(int(n))

		elif self.percent < percent:
			# go right
			n = ONEHALFSTEP * abs(percent - self.percent)
			print n
			self.percent = percent
			self.right(int(n))
		
	

	def step1(self):
		GPIO.output(self.pins[3], True)
		sleep (TIME)
		GPIO.output(self.pins[3], False)
	
	def step2(self):
		GPIO.output(self.pins[3], True)
		GPIO.output(self.pins[2], True)
		sleep (TIME)
		GPIO.output(self.pins[3], False)
		GPIO.output(self.pins[2], False)
		
	def step3(self):
		GPIO.output(self.pins[2], True)
		sleep (TIME)
		GPIO.output(self.pins[2], False)
		
	def step4(self):
		GPIO.output(self.pins[1], True)
		GPIO.output(self.pins[2], True)
		sleep (TIME)
		GPIO.output(self.pins[1], False)
		GPIO.output(self.pins[2], False)
	
	def step5(self):
		GPIO.output(self.pins[1], True)
		sleep (TIME)
		GPIO.output(self.pins[1], False)
	
	def step6(self):
		GPIO.output(self.pins[0], True)
		GPIO.output(self.pins[1], True)
		sleep (TIME)
		GPIO.output(self.pins[0], False)
		GPIO.output(self.pins[1], False)
	
	def step7(self):
		GPIO.output(self.pins[0], True)
		sleep (TIME)
		GPIO.output(self.pins[0], False)
		
	def step8(self):
		GPIO.output(self.pins[3], True)
		GPIO.output(self.pins[0], True)
		sleep (TIME)
		GPIO.output(self.pins[3], False)
		GPIO.output(self.pins[0], False)
