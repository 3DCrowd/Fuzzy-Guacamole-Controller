from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os
import threading
import printerSerial
import getPort
import time

app = Flask(__name__)
CORS(app)

### Setup ###
UPLOAD_DIR = '/home/pi/fuzzy-guacamole/files'

time.sleep(10)

PORT = getPort.getPrinterPort()

printer = printerSerial.printer(PORT)

### Printing ###
@app.route('/api/v2/print/gcode', methods=['POST'])
def printGcode ():
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
    info = printer.info
    return jsonify(info), 200


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True, threaded=True)
