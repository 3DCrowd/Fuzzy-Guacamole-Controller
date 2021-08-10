import logging
import os
import serial

class printer:
    def __init__(self, port, logname='PRINTER'):
        logging.basicConfig(filename='printer.log', level=logging.DEBUG)
        self.logname = logname

        self.ser = serial.Serial(port)
        self.ser.baudrate = 115200
        self.ser.timeout = 5
        time.sleep(5)
        self.readFromSerial()

    def readFromSerial(self, forever=False):
        while True:
            output = self.ser.read_until('\n', 1000)
            logging.info (f'{self.logname}:{output[:-1]}')
            if len(output) == 0 and not forever:
                logging.info (f'{self.logname}:Nothing More')
                break

    def sendCommand(self, command):
        ret = self.ser.write(command.encode())
        logging.info (f'{self.logname}:Sending {command}')
        return ret

    def closeConnection(self):
        self.ser.close()

    def listTodos(self):
        self.ROOT_DIR = rootDir
        self.TODO_DIR = '/todo'
        self.INPROGRESS_DIR = "/inprogress"
        self.DONE_DIR = "/done"

        self.printer = printer

        print (os.listdir(self.ROOT_DIR + self.TODO_DIR))
