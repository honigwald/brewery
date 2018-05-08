from Stepper import Stepper
from time import sleep

GPIO_STEPPER = [6,13,19,26]

s = Stepper(GPIO_STEPPER)


#s.right(3)

s.halfcircle(100)
print s.percent
sleep(1)
s.halfcircle(0)
print s.percent
sleep(1)
s.halfcircle(50)
print s.percent
sleep(1)
s.halfcircle(25)
print s.percent
sleep(1)
s.halfcircle(75)
print s.percent
sleep(1)
s.halfcircle(0)
print s.percent



print "Hello World"
