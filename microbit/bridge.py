from microbit import *
import microbit
import DFDriver
import DFMotor
import DFServo
import math

# motor =DFMotor()


receive_string = ""
# is_send = True
stop = False
uart.init(baudrate=115200)
button_a_state = False
button_b_state = False


def msg_decode(message):
    # temp = message.strip().replace("\n", "").replace("\r", "")
    _send_msg("3" + message[1:8])
    # if len(temp) == 8:
    #     if temp[0] == "0" or temp[0] == "1":
    #         set_motor(temp)
    #     elif temp[0] == "2":
    #         servo(temp)
    #     elif temp[0] == "3":
    #         digital_read_write(temp)
    #     elif temp[0] == "4":
    #         analog_read_write(temp)
    #     else:
    #         other_operate(temp)


# def set_motor(speed_message):
#     one_motor(1, speed_message[:4])
#     one_motor(3, speed_message[4:])


# def one_motor(motor_id, motor_message):
#     direction = None
#     if motor_message[0] == "0":
#         direction = motor.cw
#     else:
#         direction = motor.ccw
#     motor.speed(int(motor_message[1:]))
#     motor.run(motor_id, direction)


# def servo(servo_message):
#     servo_id = int(servo_message[4:])
#     angle = int(servo_message[1:5])
#     s = DFServo(servo_id)
#     s.angle(angle)


# def digital_read_write(digital_message):
#     if digital_message[3:5] != "99":
#         pin = _get_pin(digital_message[3:5])
#         _send_msg(str(pin.read_digital()) + "\n")

#     if digital_message[5:7] != "99":
#         pin = _get_pin(digital_message[5:7])
#         pin.write_digital(int(digital_message[7]))


# def _get_pin(pin_index_string):
#     pin_number = int(pin_index_string)
#     pin = eval("pin{}".format(pin_number))
#     return pin


# def analog_read_write(analog_message):
#     if analog_message[1:3] != "99":
#         pin = _get_pin(analog_message[1:3])
#         _send_msg(str(_map(pin.read_analog(), 0, 1024, 0, 255)) + "\n")
#     if analog_message[3:5] != "99":
#         pin = _get_pin(analog_message[3:5])
#         pin.write_analog(_map(int(analog_message[5:], 0, 255, 0, 1024)))


# def other_operate(message):
#     pass


# def _map(x, in_min, in_max, out_min, out_max):
#     return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min


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
        if button_b_state:
            _send_msg("30000110")
            button_b_state = False


while not stop:
    if uart.any():
        receive_string = str(uart.readline())

    if len(receive_string) > 0:
        msg_decode(receive_string)
        receive_string = ""
    check_button()