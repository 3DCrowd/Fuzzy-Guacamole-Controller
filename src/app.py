from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/logs', methods=['GET'])
def logs():
    try:
        with open("/var/www/html/printer.log") as f:
            printerLogs = f.readlines()
            printerLogs.reverse()
            print (printerLogs)
    except Exception as e:
        return render_template('logs.html', error=True, message=e)

    return render_template('logs.html', error=False, printerLogs=printerLogs)
