import lib.List as l
import lib.Sensor as s
import lib.Timer as t
import time
import timeit

############################################################################


def brewing(Node):
	targetTemp = Node.getData()[0]
	tStart = time.ctime()
	tEnd = Node.getData()[2]
	duration = Node.getData()[3]
	currTemp = s1.getTemprature()

	if duration == -1:
		# heat up
		print "Heating up: Start"
		time.sleep(1)
		while currTemp < targetTemp:
			print "Heating Up: [%i/%i]" % (currTemp, targetTemp)
			time.sleep(2)
			currTemp = s1.getTemprature()
		print "Heating up: Finished"
		time.sleep(1)
	else:
		# hold temprature
		print "Hold Temprature: Start"
		time.sleep(1)
		timer = t.Timer()
		timer.start(duration)
		while timer.isRunning():
			print "Hold Temprature: [%i/%i]" % (timer.getRuntime(), duration)
			timer.tick()
		print "Hold Temprature: Finished"
		time.sleep(1)

# STEP = [TARGET-TEMP, START-TIME, END-TIME, DURATION]
# this array stores the values for each step given by recipe
step = [0, 0, 0, 0]
#
## init list
finished, brew = l.List(), l.List()
brew.append([10, -1, -1, -1])
brew.append([10, -1, -1, 20])
brew.append([20, -1, -1, -1])
brew.append([20, -1, -1, 27])


tend = time.ctime()

s1 = s.Sensor(1, "sensordata")

#brew.printList()

elem = brew.head
stepNr = 0

while elem != None:
	stepNr = stepNr + 1
	print "Step: %i\t Node: %s" % (stepNr, elem)
	brewing(elem)
	elem = elem.getNext()
	print ""
