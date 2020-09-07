from car_serial import CarSerial
import time
import serial
import threading


class GenericSerial(CarSerial):

    def __init__(self, port, baud_rate=115200, callback=None):
        super(GenericSerial, self).__init__(port=port, baud_rate=baud_rate, receive=False)
        self.callback = callback
        time.sleep(0.5)
        self.ser.write("90000000\n".encode("ascii"))
        self.is_listen = True
        t = threading.Thread(target=self._receive, daemon=True)
        t.start()

    def _receive(self):
        """
                    监听Arduino端口发回的信息。
                """
        print("_listen start:")
        while self.is_listen:
            try:
                temp_str = self.ser.readline().decode("ascii")
                if temp_str != "":
                    self.callback(temp_str)
                    print("read:", temp_str)
            except serial.SerialException as e:
                # There is no new data from serial port
                print("Error:serial.SerialException")
            except TypeError as e:
                print("Error:serial.TypeError")
                return None
            else:
                pass
