class PID:
    def __init__(self, target_temp):
        self.p_fact = 98.427496492122
        self.i_fact = 0.6635561561266685 * 0.5
        self.i_total = 0.0
        self.d_fact = 230.52755757365532 * 0.3
        self.last_error = None
        self.target_temp = target_temp

    def update(self, curr_temp):
        error = self.target_temp - curr_temp
        if self.last_error == None:
            self.last_error = error
        self.i_total += error
        PID = (error * self.p_fact)
        PID += ((error - self.last_error) * self.d_fact)
        PID += (self.i_total * self.i_fact)
        PID += (self.i_fact)
        self.last_error = error

        return PID
