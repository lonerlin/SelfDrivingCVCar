from microbit import *
import microbit
import DFDriver
import DFMotor
import DFServo
import math
# motor =DFMotor()
rs = ""
stop = False
uart.init(baudrate=115200)
bas = False
bbs = False
def msg_decode(msg):
    t = msg.strip().replace("\n", "").replace("\r", "")
    _send_msg("3" + msg[1:8])
    if len(t) == 8:
        if t[0] == "0" or t[0] == "1":
            set_motor(t)
        elif t[0] == "2":
            servo(t)
        elif t[0] == "3":
            drw(t)
        elif t[0] == "4":
            arw(t)
        else:
            op(t)
def set_motor(sm):
    mot(1, sm[:4])
    mot(3, sm[4:])
def mot(mid, msg):
    dir = None
    if msg[0] == "0":
        dir = motor.cw
    else:
        dir = motor.ccw
    motor.speed(int(msg[1:]))
    motor.run(mid, dir)
def servo(msg):
    sid = int(msg[4:])
    angle = int(msg[1:5])
    s = DFServo(sid)
    s.angle(angle)
def drw(msg):
    if msg[3:5] != "99":
        pin = _get_pin(msg[3:5])
        _send_msg(str(pin.read_digital()) + "\n")
    if msg[5:7] != "99":
        pin = _get_pin(msg[5:7])
        pin.write_digital(int(msg[7]))
def _get_pin(p):
    num = int(p)
    pin = eval("pin{}".format(num))
    return pin
def arw(msg):
    if msg[1:3] != "99":
        pin = _get_pin(msg[1:3])
        _send_msg(str(_map(pin.read_analog(), 0, 1024, 0, 255)) + "\n")
    if msg[3:5] != "99":
        pin = _get_pin(msg[3:5])
        pin.write_analog(_map(int(msg[5:], 0, 255, 0, 1024)))
def op(msg):
    pass
def _map(x, in_min, in_max, out_min, out_max):
    return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min
def _send_msg(message):
    uart.write(message + "\n")
def cb():
    global bas
    global bbs
    if button_a.is_pressed() and not bas:
        _send_msg("30000051")
        bas = True
    else:
        if bas:
            bas = False
            _send_msg("30000050")
    if button_b.is_pressed() and not bbs:
        _send_msg("30000111")
        bbs = True
    else:
        if bbs:
            _send_msg("30000110")
            bbs = False
while not stop:
    if uart.any():
        rs = str(uart.readline())
    if len(rs) > 0:
        msg_decode(rs)
        rs = ""
    cb()