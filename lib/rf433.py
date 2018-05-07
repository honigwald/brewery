from subprocess import call

class Rf433:
	def on(self):
		call(["rf433/control", "1"])

	def off(self):
		call(["rf433/control", "0"])
