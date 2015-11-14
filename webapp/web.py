from flask import Flask
from flask import render_template
from flask import request

from logging.handlers import RotatingFileHandler
from ocr import retrieve_delivery_status

import hashlib
import logging
import re
import time
import xml.etree.ElementTree as ET

app = Flask(__name__)
TOKEN = 'fanshaohua'
rsp = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%d</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>'''

def valid_sign():
    signature = request.args.get('signature').encode("utf-8")
    timestamp = request.args.get('timestamp').encode("utf-8")
    nonce = request.args.get('nonce').encode("utf-8")

    lst = [TOKEN, timestamp, nonce]
    lst.sort()

    tmp_str = ''.join(lst)
    tmp_str = hashlib.sha1(tmp_str).hexdigest()

    return True if tmp_str == signature else False

def parse():
    root = ET.fromstring(request.data)
    message = {}
    for child in root:
        message[child.tag] = child.text
    return message


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        wx_msg = parse()

        app.logger.debug('http post data: %s;%s;%s;%s;%s;%s' % (wx_msg['FromUserName'], wx_msg['ToUserName'], 
            wx_msg['CreateTime'], wx_msg['MsgType'], wx_msg['MsgId'], wx_msg['Content']))

        if re.match('EA\d{9}NL', wx_msg['Content']):
            status = retrieve_delivery_status(wx_msg['Content'])
            return rsp % (wx_msg['FromUserName'], wx_msg['ToUserName'], int(time.time()), wx_msg['MsgType'], status)

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
    # app.logger.debug('tmp_str: %s', tmp_str)
