from labequipment import arduino
import time

motorbox = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55735323935351809202-if00"

class PushButtons():
    def __init__(self):
        """ Initialise with an instance of arduino.Arduino"""
        self.ard = arduino.Arduino(port=motorbox, wait=True)

    def move_motor(self, motor_no, direction):
        """
        Generate the message to be sent to self.ard.send_serial_line
        Inputs:
        motor_no: 1, 2 or 3
        direction: either 'f', 'b' or 'stop'
        """
        message = str(motor_no) + direction
        self.ard.send_serial_line(message)



test1 = PushButtons()
test1.move_motor(1, 'f')
test1.move_motor(2, 'stop')
test1.move_motor(3, 'stop')