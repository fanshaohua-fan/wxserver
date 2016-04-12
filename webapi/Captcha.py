# -*- coding: utf-8 -*-
import pytesseract
from PIL import Image
from io import BytesIO
import httplib2
import json

class Captcha(object):

    def __init__(self, url):
        self.url = url

    def ocr(self):
        h = httplib2.Http('.cache')
        response, content = h.request(self.url)
        self.cookie = response.get('set-cookie')

        image = Image.open(BytesIO(content)) 
        self.result = pytesseract.image_to_string(image)
        
        self.status = 200
        self.msg = "OK"

    def json(self):

        response = {'status': self.status,
                    'msg': self.msg,
                    'cookie': self.cookie,
                    'result': self.result }

        return json.dumps(response, sort_keys=True)

