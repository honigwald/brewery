#!/usr/bin/python3

from ..lib.rflib import RFDevice
import configparser

class Rf433:
    def __init__(self, ID, PIN, rf_codes):
        self.pin = int(PIN)
        self.pid = int(ID)
        self.repeat = 10
        self.prot = 4
        self.pulse = 355
        self.codeon = int(rf_codes[0])
        self.codeoff = int(rf_codes[1])

    def learn(self):
        self.off(plug)

    def forget(self):
        self.off(plug)

    def on(self): 
        rf = RFDevice(self.pin)
        rf.enable_tx()
        rf.tx_repeat = self.repeat
        rf.tx_code(self.codeon, self.prot, self.pulse, None)
        rf.cleanup()

    def off(self): 
        rf = RFDevice(self.pin)
        rf.enable_tx()
        rf.tx_repeat = self.repeat
        rf.tx_code(self.codeoff, self.prot, self.pulse, None)
        rf.cleanup()
