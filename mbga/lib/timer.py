import timeit
import time

class Timer:
    def __init__(self):
        self.stime = 0
        self.etime = 0
        self.runtime = 0 
        self.duration = None
        self.running = False

    def start(self, duration):
        if duration != None:
            self.duration = duration
            self.stime = timeit.default_timer()
            self.running = True
        else:
            print("Usage: start(seconds)")

    def stop(self):
        self.etime = timeit.default_timer()
        self.duration = self.etime - self.stime
        self.running = False

    def getRuntime(self):
        return self.runtime

    def tick(self): 
        if self.running == True:
            self.runtime = timeit.default_timer() - self.stime
            if self.runtime > self.duration:
                self.stop()
                print("Timer finished!")
        else:
            print("Error: Timer isn't running")
        time.sleep(1)

    def isRunning(self):
        return self.running
