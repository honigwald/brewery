class Sensor:
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
					#self.value = int(file.readline())
					content = file.readlines()
					self.value = float(content[1].split("=")[1])
					self.value /= 1000
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