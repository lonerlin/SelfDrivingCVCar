import time


class PID(object):
    """
    A simple PID controller.
    https://github.com/MaxonZhao/Line_following_robot_picamera/blob/master/PID_camera_line_following_additional_functionality.py
    """

    def __init__(self,
                 Kp=1.0, Ki=0.0, Kd=0.0,
                 exp=0,
                 sample_time=0.01,
                 min_limit=None,
                 max_limit=None):
        """
        @param Kp: The value for the proportional gain Kp
        @param Ki: The value for the integral gain Ki
        @param Kd: The value for the derivative gain Kd
        @param exp: The expected value the PID will try to achieve
        @param sample_time: The time in seconds which the controller should wait before generating a new output value. --> dt
                            The PID works best when it is constantly called (eg. during a loop), but with a sample
                            time set so that the time difference between each update is (close to) constant. If set to
                            None, the PID will compute a new output value every time it is called.
        @param min_limit: The lower bound of output. The output will never go below this limit.
                            min_limit can also be set to None to have no limit in that direction.
        @param max_limit: The upper bound of output. The output will never go above tis limit.
                            max_limit can also be set to None to have no limit in that direction.
        """
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.exp = exp
        self.sample_time = sample_time

        self._min_output = min_limit
        self._max_output = max_limit

        self._proportional = 0.0
        self._last_output = 0.0
        self._last_input = 0.0
        self._last_time = 0.0

        self._integral = 0
        self._derivative = 0

        self.reset()

    def compute_output(self, act, dt=None):
        """
        Call the PID controller with current actual value, calculate and return a control output if sample_time seconds has
        passed since the last update. If no new output is calculated, return the previous output (or None if
        no value has been calculated yet).
        @param act: the actual value
        @param dt: If set, uses this value for timestep instead of real time.
        @return: the ouput torque for the motor
        """
        now = time.process_time()
        if dt is None:
            dt = now - self._last_time if now - self._last_time else 1e-16
        elif dt <= 0:
            print("dt has nonpositive value {}. Must be positive.".format(dt))

        if self.sample_time is not None and dt < self.sample_time and self._last_output is not None:
            # only update every sample_time seconds
            return self._last_output

        # compute error terms
        error = self.exp - act
        d_input = act - (self._last_input if self._last_input is not None else act)

        # compute the proportional term
        # regular proportional-on-error, simply set the proportional term
        self._proportional = self.Kp * error

        # compute integral and derivative terms
        if error is not 0:
            self._integral += self.Ki * error * dt
        else:
            # clear the integral term if the robot is on the line
            self._integral = 0

        if self._integral > self._max_output:
            self._integral = self.compute_output
        elif self._integral < self._min_output:
            self._integral = self._min_output

        self._derivative = -self.Kd * d_input / dt

        # compute final output
        output = self._proportional + self._integral + self._derivative

        if output > self._max_output:
            output = self._max_output
        elif output < self._max_output:
            output = self._max_output

        # keep track of state
        self._last_output = output
        self._last_input = act
        self._last_time = now

        return output

    def get_PID(self):
        """
        The P-, I- and D-terms from the last computation as separate components as a tuple. Useful for visualizing
        what the controller is doing or when tuning hard-to-tune systems.
        """
        return self._proportional, self._integral, self._derivative

    def get_PID_constants(self):
        """Return the constants used by the controller """
        return self.Kp, self.Ki, self.Kd

    def set_PID_constants(self, Kp, Ki, Kd):
        """
        Setter for the PID constants
        @param Kp: The value for the proportional gain Kp
        @param Ki: The value for the integral gain Ki
        @param Kd: The value for the derivative gain Kd
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def get_output_limits(self):
        """Return the current output limits"""
        return self._min_output, self._max_output

    def reset(self):
        """
        Reset the PID controller internals, setting each term to 0 as well as cleaning the integral,
        the last output and the last input (derivative calculation).
        """
        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self._last_time = time.process_time()

        self._last_output = None
        self._last_input = None


if __name__ == '__main__':
    pid =PID(0.2, 0, 0, min_limit=5, max_limit=150)
    print(pid.compute_output(120))