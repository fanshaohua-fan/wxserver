# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from Captcha import Captcha

app = Flask(__name__)


@app.route('/ocr', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        captcha = Captcha(url)
        captcha.ocr()
        return captcha.json()

    return "success!"


if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0')

