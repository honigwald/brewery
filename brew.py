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
import json
import sys
import os

os.chdir("/home/pi/brewery")
PATHTORECIPES="web/recipes/"


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
    target_temp = int(Node.getData()[2])
    t_start = time.ctime()
    t_end = int(Node.getData()[2])
    duration = int(Node.getData()[3])
    curr_temp = s1.getTemprature()
    mypid.target_temp = target_temp


    if duration == -1:
        ### heat up
        print "Heating up: Start"
        log = open(LOGFILE, "a")
        log.write("======================\n")
        log.write(" Heating up: Start\n")
        log.write("----------------------\n")
        log.close

        sleep(1)
        while curr_temp < target_temp:
            print "Heating Up: [%iC / %iC]" % (curr_temp, target_temp)
            print "----------------------------"
            print ""
            log = open(LOGFILE, "a")
            log.write("> Heating Up: [%iC / %iC]\n" % (curr_temp, target_temp))
            log.close
            control_heating(curr_temp)
            sleep(1)
            curr_temp = s1.getTemprature()

        print "Heating up: Finished"
        log = open(LOGFILE, "a")
        log.write("----------------------\n")
        log.write(" Heating up: Finished\n")
        log.write("======================\n\n")
        sleep(1)
    else:
        ### hold temprature
        print "Hold Temprature: Start"
        log = open(LOGFILE, "a")
        log.write("===========================\n")
        log.write(" Hold Temprature: Start\n")
        log.write("---------------------------\n")
        log.close
        sleep(1)
        timer = ti.Timer()
        timer.start(duration)
        while timer.isRunning():
            print "Hold Temprature: [%iC / %iC]" % (curr_temp, target_temp)
            print "Hold Temprature: [%is / %is]" % (timer.getRuntime(), duration)
            print "----------------------------"
            print ""
            log = open(LOGFILE, "a")
            log.write("> Hold Temprature: [%iC / %iC]\n" % (curr_temp, target_temp))
            log.write("> Hold Temprature: [%is / %is]\n" % (timer.getRuntime(), duration))
            log.close

            control_heating(curr_temp)
            timer.tick()
            curr_temp = s1.getTemprature()
        print "Hold Temprature: Finished"
        log = open(LOGFILE, "a")
        log.write("---------------------------\n")
        log.write(" Hold Temprature: Finished\n")
        log.write("===========================\n\n")
        log.close
    servo1.changeAngle(0)
    sleep(2)

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
    ### check parameter
    if len(sys.argv) != 2:
        print "Error: You've to specifie a recipy"
        print "Usage: python brew.py <recipy>"
        sys.exit()

    recipy = PATHTORECIPES + sys.argv[1]
    LOGFILE="log/" + time.strftime("%Y%m%d") + "_" + "dummy" + ".txt"

    ### get current configuration
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))

    ### init list with used receipy
    ### following is still for testing purpose
    finished, brew = ls.List(), ls.List()
    with open(recipy) as f:
        data = json.load(f)

    for step in data['Step']:
        brew.append([step['name'], step['id'], step['target_temp'], step['duration']])

    elem = brew.head
    step_counter = 0

    brew.printList()

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

        log = open(LOGFILE, "a")
        ### start process
        while elem != None:
            step_counter = step_counter + 1
            print "Step: %i\t Node: %s" % (step_counter, elem)
            brewing(elem)
            elem = elem.getNext()
            print ""
        log.close()
