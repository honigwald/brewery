import lib.Thermosensor as s

SENSOR_1 = "/sys/bus/w1/devices/28-02150317c1ff/w1_slave"
#SENSOR_2 = "/sys/bus/w1/devices/28-0315040329ff/w1_slave"

s1 = s.Thermosensor(1, SENSOR_1)
#s2 = s.Sensor(2, SENSOR_2)
print s1.getTemprature()
#print s2.getTemprature()
