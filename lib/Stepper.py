import RPi.GPIO as GPIO
from time import sleep

# time needed for engine to reach estimated position
time = 0.003

class Stepper:
	def __init__(self, pins):
		self.pins = pins
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		for pin in pins:
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, False)

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

	def step1(self):
		GPIO.output(self.pins[3], True)
		sleep (time)
		GPIO.output(self.pins[3], False)
	
	def step2(self):
		GPIO.output(self.pins[3], True)
		GPIO.output(self.pins[2], True)
		sleep (time)
		GPIO.output(self.pins[3], False)
		GPIO.output(self.pins[2], False)
		
	def step3(self):
		GPIO.output(self.pins[2], True)
		sleep (time)
		GPIO.output(self.pins[2], False)
		
	def step4(self):
		GPIO.output(self.pins[1], True)
		GPIO.output(self.pins[2], True)
		sleep (time)
		GPIO.output(self.pins[1], False)
		GPIO.output(self.pins[2], False)
	
	def step5(self):
		GPIO.output(self.pins[1], True)
		sleep (time)
		GPIO.output(self.pins[1], False)
	
	def step6(self):
		GPIO.output(self.pins[0], True)
		GPIO.output(self.pins[1], True)
		sleep (time)
		GPIO.output(self.pins[0], False)
		GPIO.output(self.pins[1], False)
	
	def step7(self):
		GPIO.output(self.pins[0], True)
		sleep (time)
		GPIO.output(self.pins[0], False)
		
	def step8(self):
		GPIO.output(self.pins[3], True)
		GPIO.output(self.pins[0], True)
		sleep (time)
		GPIO.output(self.pins[3], False)
		GPIO.output(self.pins[0], False)
