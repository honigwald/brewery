import lib.List as l
import lib.Sensor as s
import lib.Timer as t
import lib.Servo as sv
import lib.rf433 as rf
from time import sleep
import time 
import timeit

############################################################################

SENSOR_2 = "/sys/bus/w1/devices/28-021502dc7eff/w1_slave"
SENSOR_1 = "/sys/bus/w1/devices/28-0315040329ff/w1_slave"
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
			print "Heating Up: [%iC / %iC]" % (currTemp, targetTemp)
			print "----------------------------"
			print ""
			#rf.on()
			servo.changeAngle(180)
			sleep(2)
			currTemp = s1.getTemprature()
		print "Heating up: Finished"
		#rf.off()
		time.sleep(1)
	else:
		# hold temprature
		print "Hold Temprature: Start"
		sleep(1)
		timer = t.Timer()
		timer.start(duration)
		while timer.isRunning():
			print "Hold Temprature: [%iC / %iC]" % (currTemp, targetTemp)
			print "Hold Temprature: [%is / %is]" % (timer.getRuntime(), duration)
			print "----------------------------"
			print ""
			if currTemp < targetTemp:
				servo.changeAngle(135)
				#rf.on()
			else:
				#rf.off()
				servo.changeAngle(45)
				#stepper.left(25)
			timer.tick()
			currTemp = s1.getTemprature()
		print "Hold Temprature: Finished"
		servo.changeAngle(0)
		#rf.off()

# STEP = [TARGET-TEMP, START-TIME, END-TIME, DURATION]
# this array stores the values for each step given by recipe
step = [0, 0, 0, 0]

# init list with used receipy
finished, brew = l.List(), l.List()
brew.append([30, -1, -1, -1])
brew.append([30, -1, -1, 300])
brew.append([35, -1, -1, -1])
brew.append([35, -1, -1, 27])

# init thermosensor
s1 = s.Sensor(1, SENSOR_1)
s2 = s.Sensor(2, SENSOR_2)
print s1.getTemprature()
print s2.getTemprature()

# init rf433 jack
#rf = rf.Rf433()
#rf.on()
#sleep(2)
#rf.off()

# init servo
servo = sv.Servo(03)
# set n:=250 for nearly one full rotation
servo.changeAngle(90)
servo.changeAngle(180)
servo.changeAngle(0)


# some further initializations
elem = brew.head
stepNr = 0


# start process
while elem != None:
	stepNr = stepNr + 1
	print "Step: %i\t Node: %s" % (stepNr, elem)
	brewing(elem)
	elem = elem.getNext()
	print ""
