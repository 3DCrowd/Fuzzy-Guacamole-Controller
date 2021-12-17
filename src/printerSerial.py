import logging
import os
import serial
import time

class printer:
    def __init__(self, port, baudrate, logname='PRINTER'):
        self.logger = logging.getLogger(logname)
        self.logger.setLevel(logging.DEBUG)

        ch = logging.FileHandler(filename='/home/pi/fuzzy-guacamole/logs/printer.log')
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(name)s:%(levelname)s:%(message)s')
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

        self.info = {
            'pos' : {'x': 0, 'y': 0, 'z': 0},
            'bedTemp': 0,
            'nozzleTemp': 0,
            'printing': False,
        }

        self.ser = serial.Serial(port)
        self.ser.baudrate = baudrate
        self.ser.timeout = 5
        self.ser.write_timeout = 5
        time.sleep(0.5)
        self.readFromSerial()

        try:
            self.ser.write(b'M115 \n')
            fullOut = ""
            for i in range(30):
                out = self.ser.readline()
                fullOut += str(out)
                self.logger.info (out)
                if out == b'ok\n':
                    self.logger.info (f'Printer responded to M115')
                    break
        except Exception as e:
            self.logger.error (f'Printer failed to respond to M115')
            raise Exception ('Not a printer')

        if len(fullOut) < 0:
           self.logger.error (f'Printer failed to respond to M115')
           raise Exception ('Not a printer')

    def readFromSerial(self, forever=False):
        while True:
            output = self.ser.read_until('\n', 1000)
            self.logger.info (f'{output[:-1]}')
            if len(output) == 0 and not forever:
                self.logger.info ('Nothing More')
                break

    def sendCommand(self, command, log=True):
        ret = self.ser.write(command.encode())
        self.unpackCommand(command)
        if log:
            self.logger.info (f'Sending {command}')
        return ret

    def getMovement(self, _command):
        command = _command[3:]
        separated = command.split()
        print (separated)
        x, y, z, speed = 0, 0, 0, 0
        for item in separated:
            if item[:1] == 'F':
                speed = item[1:]
            elif item[:1] == 'X':
                x = item[1:]
            elif item[:1] == 'Y':
                y = item[1:]
            elif item[:1] == 'Z':
                z = item[1:]

        return 'MOVEMENT', x,y,z

    def getNozzleTemp(self, _command):
        command = _command[5:]
        separated = command.split()

        for item in separated:
            if item[:1] == 'S':
                nozzle = item[1:]

                return 'NOZZLE_TEMP', nozzle

    def getBedTemp(self, _command):
        command = _command[5:]
        separated = command.split()

        self.logger.info(separated)

        for item in separated:
            if item[:1] == 'S':
                bed = item[1:]

                return 'BED_TEMP', bed

    def getInfo(self, command):
        if command[:2] == 'G0' or command[:2] == 'G1':
            return self.getMovement(command)
        elif command[:4] == 'M104' or command[:4] == 'M109':
            return self.getNozzleTemp(command)
        elif command[:4] == 'M140' or command[:4] == 'M190':
            return self.getBedTemp(command)
        elif command[:3] == 'G28':
            return 'MOVEMENT', 0, 0, 0
        else:
            return 'UNSUPPORTED_COMMAND'

    def unpackCommand(self, command):
        commandResponse = self.getInfo(command)
        if commandResponse[0] == "NOZZLE_TEMP":
            self.info['nozzleTemp'] = float(commandResponse[1])
        elif commandResponse[0] == "BED_TEMP":
            self.logger.info(commandResponse)
            self.info['bedTemp'] = float(commandResponse[1])
        elif commandResponse[0] == "MOVEMENT":
            self.info['pos']['x'] = float(commandResponse[1])
            self.info['pos']['y'] = float(commandResponse[2])
            self.info['pos']['z'] = float(commandResponse[3])

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
        self.logger.setLevel(logging.DEBUG)

        ch = logging.FileHandler(filename='/home/pi/fuzzy-guacamole/logs/printer.log')
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(name)s:%(levelname)s:%(message)s')
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

        self.fileDir = fileDir
        self.printer = printer

        #Get total lines from file
        with open(self.fileDir, 'r') as f:
            totalLines = len(f.readlines())

        self.printer.info['totalLines'] = totalLines
        self.printer.info['currentLine'] = 0
        self.printer.info['filename'] = os.path.basename(fileDir)

    def start(self):
        self.printer.info['printing'] = True

        with open (self.fileDir, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.printer.info['currentLine'] += 1

                if line[0] == ';' or line[0] == '\n':
                    self.logger.info(f"Skipping: {line[:-1]}")
                else:
                    self.logger.info (f"Sending: {line[:-1]}")
                    self.printer.sendCommand(line)

                    while True:
                        output = self.printer.ser.read_until(b'\n',1000)
                        self.logger.info(output[:-1].decode())

                        if output[:2] == b'ok':
                            self.logger.info("OK found")
                            break
        self.printer.info['printing'] = False
