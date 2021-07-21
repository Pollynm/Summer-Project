from labequipment import arduino
import time

motorbox = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55735323935351809202-if00"


class SendSerialCommands():
    def __init__(self):
        """ Initialise with an instance of arduino.Arduino"""
        self.ard = arduino.Arduino(port=motorbox, wait=True)

    def move_motors(self, motor_numbers, direction, duration=None):
        """
        Generate the message to be sent to self.ard.send_serial_line
        Inputs:
        motor_numbers: type=list, 1, 2, 3 or any combination
        direction: either 'f', 'b' or 'stop'
        duration: length of motor run (seconds)
        """
        for motors in motor_numbers:
            message = str(motors) + direction
            self.ard.send_serial_line(message)
        if duration:
            time.sleep(duration)
            for motors in motor_numbers:
                message = str(motors) + 'stop'
                self.ard.send_serial_line(message)