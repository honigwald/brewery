import lib.List as l
import lib.Sensor as s
import lib.Timer as t
import lib.Stepper as st
from time import sleep
import time 
import timeit

############################################################################

SENSOR_1 = "/sys/bus/w1/devices/28-021502dc7eff/w1_slave"
SENSOR_2 = "/sys/bus/w1/devices/28-0315040329ff/w1_slave"
GPIO_STEPPER = [6,13,19,26]

# the magic happens here
def brewing(Node):
	targetTemp = Node.getData()[0]
	tStart = time.ctime()
	tEnd = Node.getData()[2]
	duration = Node.getData()[3]
	currTemp = s1.getTemprature()

	if duration == -1:
		# heat up
		print "Heating up: Start"
		sleep(1)
		while currTemp < targetTemp:
			print "Heating Up: [%i/%i]" % (currTemp, targetTemp)
			sleep(2)
			currTemp = s1.getTemprature()
		print "Heating up: Finished"
		time.sleep(1)
	else:
		# hold temprature
		print "Hold Temprature: Start"
		sleep(1)
		timer = t.Timer()
		timer.start(duration)
		while timer.isRunning():
			print "Hold Temprature: [%i/%i]" % (timer.getRuntime(), duration)
			timer.tick()
		print "Hold Temprature: Finished"
		sleep(1)

# STEP = [TARGET-TEMP, START-TIME, END-TIME, DURATION]
# this array stores the values for each step given by recipe
step = [0, 0, 0, 0]

# init list with used receipy
finished, brew = l.List(), l.List()
brew.append([30, -1, -1, -1])
brew.append([10, -1, -1, 20])
brew.append([20, -1, -1, -1])
brew.append([20, -1, -1, 27])

# init thermosensor
s1 = s.Sensor(1, SENSOR_1)
s2 = s.Sensor(2, SENSOR_2)

# init stepper
stepper = st.Stepper(GPIO_STEPPER)
# set n:=250 for nearly one full rotation
stepper.right(25)
#stepper.left(25)

# some further initializations
elem = brew.head
stepNr = 0

# start process
'''
while elem != None:
	stepNr = stepNr + 1
	print "Step: %i\t Node: %s" % (stepNr, elem)
	brewing(elem)
	elem = elem.getNext()
	print ""
'''