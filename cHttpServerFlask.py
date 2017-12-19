from flask import Flask, render_template, Response
import time
import logging

import config

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s,%(msecs)-3d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger('fuming')


currentStatus = 'close'
currentFileName = str(int(round(time.time() * 1000)))


@app.route('/act/<name>/<fileName>')
def index(name, fileName):
    global currentStatus
    global currentFileName
    # return template('<b>Hello {{name}}</b>!', name=name)
    currentStatus = name
    currentFileName = fileName
    resp = '{"status":"' + currentStatus + \
        '","fileName":"' + currentFileName + '"}'
    f = open("cHello.ini", "w")
    f.write(resp)
    f.close()
    return '{"status": "ok"}'


@app.route('/get')
def getInfo():
    resp = '{"status":"' + currentStatus + \
        '","fileName":"' + currentFileName + '"}'
    return resp


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='localhost', port=config.GLOBAL_SETTINGS[
            'port'], debug=True)
