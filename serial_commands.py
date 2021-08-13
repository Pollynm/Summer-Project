from labequipment import arduino
import time

motorbox = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_850333131373513111A0-if00"


class SendSerialCommands():
    def __init__(self):
        """ Initialise with an instance of arduino.Arduino"""
        self.ard = arduino.Arduino(port=motorbox, wait=True)

    def move_motors(self, motor_numbers, move=None):
        """
        Generate the message to be sent to self.ard.send_serial_line
        Inputs:
        motor_numbers: type=list, 1, 2, 3 or any combination
        direction: either 'f', 'b' or 'stop'
        duration: length of motor run (seconds)
        """
        message=''
        for motors in motor_numbers:
            if move[motors - 1] > 0:
                message = str(motors) + 'f'
            elif move[motors - 1] < 0:
                message = str(motors) + 'b'
            self.ard.send_serial_line(message)
            time.sleep(abs(move[motors - 1]))
            message = str(motors) + 'stop'
            self.ard.send_serial_line(message)