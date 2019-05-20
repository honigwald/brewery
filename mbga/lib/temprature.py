import lib.Thermosensor as s
import lib.Pid as pid
import sys
import time

SENSOR_1 = "/sys/bus/w1/devices/28-02150317c1ff/w1_slave"
#SENSOR_2 = "/sys/bus/w1/devices/28-0315040329ff/w1_slave"

s1 = s.Thermosensor(1, SENSOR_1)
print(s1.getTemprature())
temp = s1.getTemprature()

mypid = pid.PID(int(sys.argv[1]))
pidvalue = mypid.update(temp)

i = 0
while i < 10:
    pidvalue = mypid.update(temp)
    print("PID: Current = %s\t Target = %s\t Value = %s" % temp, mypid.target_temp, pidvalue)
    i += 1
    time.sleep(5)

print('next')
i = 0
mypid = pid.PID(int(sys.argv[1]))
while i < 10:
    pidvalue = mypid.update(temp)
    print("PID: Current = %s\t Target = %s\t Value = %s" % temp, mypid.target_temp, pidvalue)
    i += 1
    time.sleep(1)
