
import time

class Repeat:

    def __init__(self):
        self.name_list = []
    def check(self,name):
        r_value = False
        for nl in self.name_list:
            if nl[0] == name:
                if time.perf_counter() - nl[1] > 10:
                    r_value = True
                    nl[1] = time.perf_counter()
                else:
                    r_value = False
                return r_value
                break
        self.name_list.append(name, time.perf_counter())
        return True
