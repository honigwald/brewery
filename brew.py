import lib.List as ls
import lib.Thermosensor as ts
import lib.Timer as ti
import lib.Servo as sv
import lib.rf433 as rf
import lib.pid as pid

from time import sleep
import time
import timeit
import ConfigParser

'''
++++++++++++++++++++++++++++++++++++++++++++++++
+++ Here following some function definitions +++
++++++++++++++++++++++++++++++++++++++++++++++++
'''
### TESTING MODE: Activate in config file
def testing(Node):
    print "Funktioniert"
    #P = 3.0
    #I = 0.4
    #D = 1.2
    mypid=pid.PID(37.0)
    #mypid.set_point = 40.0
    #while True:
    #     pid = p.update(measurement_value)

    servo_pin = config.getint("Servo_2", "pin")
    servo2 = sv.Servo(servo_pin)
    servo2.changeAngle(180)

    oldvalue = 0
    while True:
        '''
        if p.update(s1.getTemprature()) > 100:
            print p.update(s1.getTemprature())
            servo2.more()
        elif p.update(s1.getTemprature()) < 20:
            servo2.changeAngle(0)
            print p.update(s1.getTemprature())
        else:
            servo2.less()
        print s1.getTemprature()
        '''
        temp1 = s1.getTemprature()

        pidvalue = mypid.update(temp1)
        #diff = pidvalue - oldvalue
        print ("PID: Current = %s\t Target = %s\t Value = %s") % (temp1, mypid.target_temp, pidvalue)
        sleep(2)
        #oldvalue = pidvalue

        #if temp > 


    servo2.changeAngle(0)

    #servo_pin = config.getint("Servo_1", "pin")
    #servo1 = sv.Servo(servo_pin)

    #servo1.changeAngle(-180)
    #servo1.changeAngle(-0)
    print s1.getTemprature()

### BREWING MODE: Activate in config file. 
### the magic happens here in production mode
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

            n = 5
            if (currTemp + n) < targetTemp:
                # turn heat to maximum
                servo1.changeAngle(-180)
                servo2.changeAngle(-180)
            else:
                # slow heating process down
                servo.changeAngle(-135)
            sleep(1)
            currTemp = s1.getTemprature()
        print "Heating up: Finished"
        #rf.off()
        sleep(1)
    else:
        # hold temprature
        print "Hold Temprature: Start"
        sleep(1)
        timer = ti.Timer()
        timer.start(duration)
        while timer.isRunning():
            print "Hold Temprature: [%iC / %iC]" % (currTemp, targetTemp)
            print "Hold Temprature: [%is / %is]" % (timer.getRuntime(), duration)
            print "----------------------------"
            print ""
            if currTemp < targetTemp:
                servo1.changeAngle(-90)
                servo2.changeAngle(-90)
                #rf.on()
            else:
                servo1.changeAngle(-45)
                servo2.changeAngle(-45)
                #rf.off()
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
if __name__ == '__main__':
    print "Hello main function"
    ### get current configuration
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))

    ### this array stores the values for each step given by recipe
    ### STEP = [TARGET-TEMP, START-TIME, END-TIME, DURATION]
    step = [0, 0, 0, 0]

    ### init list with used receipy
    ### following is still for testing purpose
    finished, brew = ls.List(), ls.List()
    brew.append([50, -1, -1, -1])
    brew.append([50, -1, -1, 60])
    brew.append([60, -1, -1, -1])
    brew.append([60, -1, -1, 100])
    elem = brew.head
    step_counter = 0

    ### get running mode
    mode = config.get("Modus", "mode")

    ### no brewing but testing
    if mode == "test":
        print "TEST-MODUS"
        s1_id = 1
        s1_path = config.get("Thermo_1", "path")
        s1 = ts.Thermosensor(s1_id, s1_path)
        testing(1)

    ### time for brewing
    else:
        ### init thermosensor
        s1_id = 1
        s1_path = config.get("Thermo_1", "path")
        s1 = ts.Thermosensor(s1_id, s1_path)
        #s2 = ts.Sensor(2, SENSOR_2)

        ### init servo
        servo_pin = config.getint("Servo_1", "pin")
        servo1 = sv.Servo(servo_pin)

        servo_pin = config.getint("Servo_2", "pin")
        servo2 = sv.Servo(servo_pin)

        ### init rf433 jack
        #rf = rf.Rf433()

        ### start process
        while elem != None:
            step_counter = step_counter + 1
            print "Step: %i\t Node: %s" % (step_counter, elem)
            brewing(elem)
            elem = elem.getNext()
            print ""
