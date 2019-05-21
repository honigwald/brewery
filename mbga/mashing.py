from mbga.lib.llist     import List
from mbga.lib.timer     import Timer
from mbga.lib.pid       import PID

#from mbga.ext.tsensor   import Tsensor
#from mbga.ext.servo     import Servo
#from mbga.ext.rf433     import Rf433

from time import sleep, ctime
import timeit, configparser, json, sys, os

WORKDIR=os.path.dirname(os.path.realpath(__file__))
os.chdir(WORKDIR)

### TEST MODE: Activate in config file
def test(Node, Sensor, Rfplug):
    print("\nTEST MODE ACTIVATED")
    print("-------------------")
    print("Checking external devices...")
    print("> Temprature: %s" % Sensor.getTemprature())
    print("> RfSender: Plug on...")
    Rfplug.on()
    sleep(3)
    print("> RfSender: Plug off...")
    Rfplug.off()

    print("\nChecking linked-list...")
    print("> Head: %s" % Node)
    
    print("\nEverything looks fine")
    print("-------------------")
    sleep(3)

    mypid = PID(36.0)
    while True:
        temp = Sensor.getTemprature()
        pidvalue = mypid.update(temp)
        print("PID: Current = %s\t Target = %s\t Value = %s" % (temp, mypid.te_target, pidvalue))
        if pidvalue < 50:
            Rfplug.off()
        else:
            Rfplug.on()
        sleep(2)

### BREWING MODE: Activate in config file. 
### the magic happens here
def brew(Node, tsensor, rfplug, log):
    mypid = PID(None)
    ti_start = ctime()
    ti_end = int(Node.getData()[2])
    duration = int(Node.getData()[3])
    te_target = int(Node.getData()[2])
    te_current = tsensor.getTemprature()

    if duration == -1:
        ### heat up
        mypid.te_target = te_target
        print("======================")
        print(" Heating up: Start")
        print("----------------------")
        #log = open(LOGFILE, "a")
        log.write("======================\n")
        log.write(" Heating up: Start\n")
        log.write("----------------------\n")
        #log.close

        sleep(1)
        while te_current < te_target:
            print("> Heating Up: [%iC / %iC]" % (te_current, te_target))
            #log = open(LOGFILE, "a")
            log.write("> Heating Up: [%iC / %iC]\n" % (te_current, te_target))
            #log.close
            ctrl_heat(te_current, te_target, rfplug, mypid, log)
            sleep(1)
            te_current = tsensor.getTemprature()

        print("----------------------\n")
        print(" Heating up: Finished\n")
        print("======================\n\n")

        #log = open(LOGFILE, "a")
        log.write("----------------------\n")
        log.write(" Heating up: Finished\n")
        log.write("======================\n\n")
        sleep(1)
    else:
        ### hold temprature
        mypid.te_target = te_target
        print("Hold Temprature: Start")
        #log = open(LOGFILE, "a")
        log.write("===========================\n")
        log.write(" Hold Temprature: Start\n")
        log.write("---------------------------\n")
        #log.close
        sleep(1)
        timer = Timer()
        timer.start(duration)
        while timer.isRunning():
            print("> Hold Temprature (%is / %is): [%iC / %iC]" % timer.getRuntime(), duration, te_current, te_target)
            #log = open(LOGFILE, "a")
            log.write("> Hold Temprature (%is / %is): [%iC / %iC]\n" % (timer.getRuntime(), duration, te_current, te_target))
            #log.close

            ### if current < target then
            ctrl_heat(te_current, te_target, log)
            timer.tick()
            te_current = tsensor.getTemprature()
        print("---------------------------\n")
        print(" Hold Temprature: Finished\n")
        print("===========================\n\n")
        #log = open(LOGFILE, "a")
        log.write("---------------------------\n")
        log.write(" Hold Temprature: Finished\n")
        log.write("===========================\n\n")
        #log.close
    rfplug.off()

def ctrl_heat(te_current, te_target, rfplug, pid, log):
    pidvalue = pid.update(te_current)
    print("> PID: Current = %s\t Target = %s\t Value = %s" % (te_current, pid.te_target, pidvalue))
    log.write("> PID: Current = %s\t Target = %s\t Value = %s\n" % (te_current, pid.te_target, pidvalue))

    if te_target < 40:
        threshold = 1000
    elif te_target < 55:
        threshold = 800
    elif te_target < 65:
        threshold = 600
    else:
        threshold = 400

    if pidvalue < threshold:
        # absolute: stopheating
        rfplug.off()
    else:
        # absolute: fullpower
        rfplug.on()
    sleep(5)
