import lib.List as ls 
import lib.Thermosensor as ts
import lib.Timer as timer
import lib.Servo as sv
import lib.rf433 as rf

from time import sleep
import timeit
import ConfigParser

'''
-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Here following some function definitions |
-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''
# the magic happens here in testing mode
def testing(Node):
	print "Funktioniert"

# the magic happens here in production mode
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
			timer.tick()
			currTemp = s1.getTemprature()
		print "Hold Temprature: Finished"
		servo.changeAngle(0)
		#rf.off()
''' 
-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Some needed configurations before starting |
-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''

# get current configuration
config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))

# this array stores the values for each step given by recipe
# STEP = [TARGET-TEMP, START-TIME, END-TIME, DURATION]
step = [0, 0, 0, 0]

# init list with used receipy
finished, brew = ls.List(), ls.List()
brew.append([30, -1, -1, -1])
brew.append([30, -1, -1, 300])
brew.append([35, -1, -1, -1])
brew.append([35, -1, -1, 27])
elem = brew.head
stepNr = 0

# get running mode
mode = config.get("Modus", "mode")
# program is running in test-mode
if mode == "test":
	print "TEST-MODUS"
	testing(1)

# program is running in prod-mode
else:
	# init thermosensor
	s1Id = 1
	s1Path = config.get("Thermo_1", "path")
	ts = ts.Thermosensor(s1Id, s1Path)
	#s2 = ts.Sensor(2, SENSOR_2)

	## init servo
	servoPin = config.get("Servo_1", "pin")
	servo = sv.Servo(servoPin)

	## init rf433 jack
	#rf = rf.Rf433()

	# start process
	while elem != None:
		stepNr = stepNr + 1
		print "Step: %i\t Node: %s" % (stepNr, elem)
		brewing(elem)
		elem = elem.getNext()
		print ""


