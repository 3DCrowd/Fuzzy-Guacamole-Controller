from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os
import threading
import printerSerial
#import getPort
import serial.tools.list_ports as list_ports
import time

app = Flask(__name__)
CORS(app)

### Setup ###
UPLOAD_DIR = '/home/pi/fuzzy-guacamole/files'

#time.sleep(10)

#PORT = getPort.getPrinterPort()

printer = None
connected = False

### Connection ###
@app.route('/api/v2/connect/list', methods=['GET'])
def listPorts():
    ports = list(list_ports.comports())
    out = {'ports':[]}

    for port in ports:
        print (port.device)
        out['ports'].append(port.device)


    return out, 200

@app.route('/api/v2/connect', methods=['POST'])
def setPort():
    global printer
    global connected

    port = request.json['port']
    baudrate = int(request.json['baudrate'])

    if port != '':
        try:
            printer = printerSerial.printer(port, baudrate)
            connected = True
            return jsonify({'status': 'success'}), 202
        except Exception as e:
            print(e)
            return abort(500, 'Failed to connect to port. Please check if you printer is connected')
    else:
        return abort(400, 'Please provide a port')

### Printing ###
@app.route('/api/v2/print/gcode', methods=['POST'])
def printGcode ():
    if not connected:
        return abort(503, 'Printer is Disconnected')

    file = request.files['file']

    fileExtension = os.path.splitext(file.filename)[1]

    if file.filename != '':
        if fileExtension == ".gcode" or fileExtension == ".GCODE":
            file.save(os.path.join(UPLOAD_DIR, file.filename))

            printjob = printerSerial.job(os.path.join(UPLOAD_DIR, file.filename), printer)
            threading.Thread(target=lambda: printjob.start()).start()

            return jsonify({'status': 'success'}), 201
        else:
            return abort(400, 'Please provide a gcode file')

    else:
        return abort(400, 'Please provide a file')

### Info ###
@app.route('/api/v2/info', methods=['GET'])
def getInfo ():
    if not connected:
        return abort(503, 'Printer is Disconnected')

    info = printer.info

    if not info['printing']:
        #Send alive check if not printing
        printer.sendCommand(';\n', False)

    return jsonify(info), 200


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True, threaded=True)
