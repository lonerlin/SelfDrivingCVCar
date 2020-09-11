from microbit import *
import microbit
receive_string = ""
is_send = True
stop = False
uart.init(baudrate=115200)
button_a_state = False
button_b_state = False


def msg_decode(message):
    temp = message.strip().replace("\n", "").replace("\r", "")
    if len(temp) == 8:
        if temp[0] == "0" or temp[0] == "1":
            motor(temp)
        elif temp[0] == "2":
            servo(temp)
        elif temp[0] == "3":
            digital_read_write(temp)
        elif temp[0] == "4":
            analog_read_write(temp)
        else:
            other_operate(temp)


def motor(speed_message):
    pass


def servo(servo_message):
    pass


def digital_read_write(digital_message):
    if digital_message[3:5] != "99" :
        _send_msg(pin)


def analog_read_write(analog_message):
    pass


def other_operate(message):
    pass


def _map(x, in_min, in_max, out_min, out_max):
    return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min


def _send_msg(message):
    uart.write(message + "\n")


def check_button():
    global button_a_state
    global button_b_state
    if button_a.is_pressed():
        _send_msg("30000051")
        button_a_state = True
    else:
        if button_a_state:
            button_a_state = False
            _send_msg("30000050")
    if button_b.is_pressed():
        _send_msg("30000111")
        button_b_state = True
    else:
        if button_a_state:
            _send_msg("30000110")
            button_b_state = False


while not stop:
    if uart.any():
        receive_string = uart.readline()
    if len(receive_string) > 0:
        msg_decode(receive_string)
        check_button()


