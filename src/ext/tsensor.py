convertToDegree = 1000

class Tsensor:
    def __init__(self, id, filehandler):
        self.id = id 
        self.filehandler = filehandler
        self.value = None

    def getTemprature(self):
        if self.filehandler == None:
            return None
        else:
            nextTry = 0
            while nextTry < 3:
                try:
                    file = open(self.filehandler)
                    content = file.readlines()
                    self.value = float(content[1].split("=")[1])
                    self.value /= convertToDegree
                    break
                except (IOError):
                    print "IOError: File not found"
                except (ValueError):
                    print "ValueError: Expect integer"
                file.close()
                nextTry = nextTry + 1
                if nextTry < 3:
                    file.close()
            return self.value

    def printStatistic(self):
        print "Sensor ID: %i\t Temprature: %i" % (self.id, self.value) 


if __name__ == '__main__':
    s1_id = 1
    s1_path = "/sys/bus/w1/devices/28-02150317c1ff/w1_slave"
    s1 = Thermosensor(s1_id, s1_path)
    print s1.getTemprature()
