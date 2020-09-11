from car_serial import CarSerial
import time
import serial
import threading


class GenericSerial(CarSerial):

    def __init__(self, port, baud_rate=115200, digital_callback=None, analog_callback=None, callback=None):
        super(GenericSerial, self).__init__(port=port, baud_rate=baud_rate, receive=False)
        self.digital_callback = digital_callback
        self.analog_callback = analog_callback
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
                    self._decode(temp_str)
                    print("read:", temp_str)
            except serial.SerialException as e:
                # There is no new data from serial port
                print("Error:serial.SerialException")
            except TypeError as e:
                print("Error:serial.TypeError")
                return None
            else:
                pass

    def _decode(self, command: str):
        temp = command.strip().replace("\n", "").replace("\r", "")
        if len(temp) == 8:
            if temp[0] == "3" and self.digital_callback is not None:
                self.digital_callback(temp[1:])
            elif temp[0] == "4" and self.analog_callback is not None:
                self.analog_callback(temp[1:])
            else:
                self.callback(temp)
