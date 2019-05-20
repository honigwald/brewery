from mbga import mashing
from mbga.lib.llist import List
from mbga.ext.tsensor import Tsensor
from mbga.ext.rf433 import Rf433

import sys, time, configparser, json, os

recipe_store="web/recipes/"
workdir=os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    ### check parameter
    if len(sys.argv) != 2:
        print("Error: You've to specify a recipe")
        print("Usage: python -m mbga <recipe>")
        sys.exit()

    recipe = recipe_store + sys.argv[1]
    logfile="log/" + time.strftime("%Y%m%d") + "_" + "dummy" + ".txt"

    ### get configuration flags
    config = configparser.ConfigParser()
    config.readfp(open('config.ini'))

    ### init list
    finished, todo = List(), List()
    with open(recipe) as f:
        data = json.load(f)

    for step in data['Step']:
        todo.append([step['name'], step['id'], step['target_temp'], step['duration']])

    ### get running mode
    mode = config.get("Mode", "mode")

    elem = todo.head
    step_counter = 0

    ### init rf433 plugs
    rf_pin = config.get("RfSender", "pin")
    rf_raw_codes = config.get("RfSender", "codes")
    items = rf_raw_codes
    items = items.replace('\n', '').replace('[','')
    items = items.replace(']', '').split(';')
    rf_codes = []
    for item in items:
        code = item.replace('(','').replace(')','').split(',')
        rf_codes.append(list(map(int,code)))
    rf1 = Rf433(0, rf_pin, rf_codes[0])

    ### testmode
    if mode == "test":
        s1_id = 1
        s1_path = config.get("Thermo_1", "path")
        s1 = Tsensor(s1_id, s1_path)
        mashing.test(elem, s1, rf1)

    ### brewmode
    else:
        ### init thermosensor
        s1_id = 1
        s1_path = config.get("Thermo_1", "path")
        s1 = Tsensor(s1_id, s1_path)
        #s2 = ts.Sensor(2, SENSOR_2)
        
        ### init pid
        mypid = PID(None)

        ### init servo
        servo_pin = config.getint("Servo_1", "pin")
        servo1 = Servo(servo_pin)

        #servo_pin = config.getint("Servo_2", "pin")
        #servo2 = sv.Servo(servo_pin)

        ### init rf433 jack
        #rf = rf.Rf433()

        log = open(logfile, "a")
        ### start process
        while elem != None:
            step_counter = step_counter + 1
            print("Step: %i\t Node: %s" % step_counter, elem)
            brew(elem)
            elem = elem.getNext()
            print("")
        log.close()
