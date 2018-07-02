import lib.List as ls
import lib.Thermosensor as ts
import lib.Timer as ti
import lib.Servo as sv
import lib.rf433 as rf
import lib.Pid as pid

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
    print "TESTING MODE ACTIVATED"
    mypid=pid.PID(37.0)

    servo_pin = config.getint("Servo_1", "pin")
    servo1 = sv.Servo(servo_pin)
    servo1.changeAngle(180)

    while True:
        temp1 = s1.getTemprature()
        pidvalue = mypid.update(temp1)
        print ("PID: Current = %s\t Target = %s\t Value = %s") % (temp1, mypid.target_temp, pidvalue)
        sleep(2)

        if abs(pidvalue) < 5:
            # absolute: stopheating
            servo1.changeAngle(0)
        elif abs(pidvalue) < 7:
            # absolute: slowest heating
            servo1.changeAngle(22.5)
        elif abs(pidvalue) < 10:
            # relative: slower heating
            servo1.less()
        else:
            # absolute: fullpower
            servo1.changeAngle(180)



### BREWING MODE: Activate in config file. 
### the magic happens here in production mode
def brewing(Node):
    target_temp = Node.getData()[0]
    t_start = time.ctime()
    t_end = Node.getData()[2]
    duration = Node.getData()[3]
    curr_temp = s1.getTemprature()
    mypid.target_temp = target_temp

    if duration == -1:
        ### heat up
        print "Heating up: Start"
        sleep(1)
        while curr_temp < target_temp:
            print "Heating Up: [%iC / %iC]" % (curr_temp, target_temp)
            print "----------------------------"
            print ""
            control_heating(curr_temp)
            sleep(1)
            curr_temp = s1.getTemprature()

        print "Heating up: Finished"
        sleep(1)
    else:
        ### hold temprature
        print "Hold Temprature: Start"
        sleep(1)
        timer = ti.Timer()
        timer.start(duration)
        while timer.isRunning():
            print "Hold Temprature: [%iC / %iC]" % (curr_temp, target_temp)
            print "Hold Temprature: [%is / %is]" % (timer.getRuntime(), duration)
            print "----------------------------"
            print ""
            control_heating(curr_temp)
            timer.tick()
            curr_temp = s1.getTemprature()
        print "Hold Temprature: Finished"
    servo1.changeAngle(0)

def control_heating(curr_temp):
    pidvalue = mypid.update(curr_temp)
    print ("PID: Current = %s\t Target = %s\t Value = %s") % (curr_temp, mypid.target_temp, pidvalue)
    if abs(pidvalue) < 5:
        # absolute: stopheating
        servo1.changeAngle(0)
    elif abs(pidvalue) < 7:
        # absolute: slowest heating
        servo1.changeAngle(22.5)
    elif abs(pidvalue) < 10:
        # relative: slower heating
        servo1.less()
    else:
        # absolute: fullpower
        servo1.changeAngle(180)

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
        
        ### init pid
        mypid = pid.PID(None)

        ### init servo
        servo_pin = config.getint("Servo_1", "pin")
        servo1 = sv.Servo(servo_pin)

        #servo_pin = config.getint("Servo_2", "pin")
        #servo2 = sv.Servo(servo_pin)

        ### init rf433 jack
        #rf = rf.Rf433()

        ### start process
        while elem != None:
            step_counter = step_counter + 1
            print "Step: %i\t Node: %s" % (step_counter, elem)
            brewing(elem)
            elem = elem.getNext()
            print ""
