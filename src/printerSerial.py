import logging
import os
import serial
import time

class printer:
    def __init__(self, port, logname='PRINTER'):
        self.logger = logging.getLogger(logname)

        ch = logging.FileHandler(filename='printer.log')
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)


        self.ser = serial.Serial(port)
        self.ser.baudrate = 115200
        self.ser.timeout = 5
        time.sleep(5)
        self.readFromSerial()

    def readFromSerial(self, forever=False):
        while True:
            output = self.ser.read_until('\n', 1000)
            self.logger.info (f'{output[:-1]}')
            if len(output) == 0 and not forever:
                self.logger.info ('Nothing More')
                break

    def sendCommand(self, command):
        ret = self.ser.write(command.encode())
        self.logger.info (f'Sending {command}')
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

class job:
    def __init__(self, fileDir, printer):
        self.logger = logging.getLogger(os.path.basename(fileDir)[:-6])

        ch = logging.FileHandler(filename='printer.log')
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

        self.fileDir = fileDir
        self.printer = printer

        self.info = {
            'pos' : {'x': 0, 'y': 0, 'z': 0},
            'bedTemp': 0,
            'nozzleTemp': 0,
            'currentLine': 0,
        }

        #Get total lines from file
        with open(self.fileDir, 'r') as f:
            totalLines = len(f.readlines())

        self.info['totalLines'] = totalLines


    def start(self):
        with open (self.fileDir, 'r') as f:
            for line in f:
                if line[0] == ';' or line[0] == '\n':
                    self.logger.info(f"Skipping: {line[:-1]}")
                else:
                    self.logger.info (f"Sending: {line[:-1]}")
                    self.printer.sendCommand(line)
