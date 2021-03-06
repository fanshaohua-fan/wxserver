# -*- coding: utf-8 -*-
from base import app
from base import db
from model import WeChatMessage
from model import WeChatEvent
from flask import request
from kuaidi import kuaidi_oto, kuaidi_ems, kuaidi_euasia

from logging.handlers import RotatingFileHandler

import hashlib
import logging
import re
import time
import xml.etree.ElementTree as ET


rsp = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%d</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>
'''


def valid_sign():
    signature = request.args.get('signature').encode("utf-8")
    timestamp = request.args.get('timestamp').encode("utf-8")
    nonce = request.args.get('nonce').encode("utf-8")

    lst = [app.config['TOKEN'], timestamp, nonce]
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

        app.logger.debug('http post data: %s;%s;%s;%s' % (
            wx_msg['FromUserName'],
            wx_msg['ToUserName'],
            wx_msg['CreateTime'],
            wx_msg['MsgType']
            ))

        if wx_msg['MsgType'] == 'event':
            db_msg = WeChatEvent(**wx_msg)
        else:
            db_msg = WeChatMessage(**wx_msg)

        try:
            db.session.add(db_msg)
            db.session.commit()
        except Exception as e:
            pass

        if 'Content' in wx_msg.keys():
            content = wx_msg['Content'].upper().strip()

            delivery = None
            if re.match('\d{11}[A-Z]\d', content):
                delivery = kuaidi_oto(content)
            elif re.match('EA\d{9}NL', content):
                delivery = kuaidi_ems(content)
            elif re.match('EAXON\d{7}', content):
                delivery = kuaidi_euasia(content)
            else:
                pass

            if delivery is not None:
                status = delivery.status()
                app.logger.debug('%s status:\n%s', delivery.name, status)
                return rsp % (
                    wx_msg['FromUserName'],
                    wx_msg['ToUserName'],
                    int(time.time()),
                    wx_msg['MsgType'],
                    status)

        return "success"

    timestamp = request.args.get('timestamp')
    if timestamp is None:
        return "success"

    return request.args.get('echostr') if valid_sign() else "verification failed!"

if __name__ == '__main__':

    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0')

