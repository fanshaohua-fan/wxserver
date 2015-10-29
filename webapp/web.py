from flask import Flask
from flask import render_template
from flask import request

import hashlib
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
TOKEN = 'fanshaohua'

def valid_sign():
    signature = request.args.get('signature').encode("utf-8")
    timestamp = request.args.get('timestamp').encode("utf-8")
    nonce = request.args.get('nonce').encode("utf-8")

    app.logger.debug('signature: %s', signature)
    app.logger.debug('timestamp: %s', timestamp)
    app.logger.debug('nonce: %s', nonce)

    token = TOKEN

    lst = [token, timestamp, nonce]
    lst.sort()
    tmp_str = ''.join(lst)

    tmp_str = hashlib.sha1(tmp_str).hexdigest()
    app.logger.debug('tmp_str: %s', tmp_str)

    if tmp_str == signature :
        return True
    else:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return "success"

    timestamp = request.args.get('timestamp')
    if timestamp is None:
        return "success"

    return request.args.get('echostr') if valid_sign() else "verification failed!"

if __name__ == '__main__':
    app.debug = True

    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0')
