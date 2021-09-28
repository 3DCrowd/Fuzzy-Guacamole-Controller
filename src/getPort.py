import serial.tools.list_ports as list_ports
import serial
import time
import logging

logger = logging.getLogger('GetPort')
logger.setLevel(logging.DEBUG)

ch = logging.FileHandler(filename='/home/pi/fuzzy-guacamole/logs/printer.log')
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)s:%(levelname)s:%(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)


def getPrinterPort():
    ports = list(list_ports.comports())

    for port in ports:
        logger.info(f"{port.name}: {port.description}: {port.manufacturer}")

        with serial.Serial(port.device, 115200, timeout=0, writeTimeout=5) as ser:
            try:
                ser.write(b'M115 \n')
                fullOut = ""
                for i in range(30):
                    out = ser.readline()
                    fullOut += str(out)
                    logger.info (out)
                    if out == b'ok\n':
                        logger.info (f'Port {port.name} is a printer')
                        return port.device
                if len(fullOut) < 0:
                   raise Exception ('Not a printer')
            except Exception as e:
                logger.exception (e)
                logger.info (f'Tried port {port.name}')
                pass

if __name__ == "__main__":
    print (getPrinterPort())
