# -*- coding: utf-8 -*-
import pytesseract
from PIL import Image
from StringIO import StringIO
from urllib import urlencode
from lxml import html
import httplib2


#httplib2.debuglevel = 1
h = httplib2.Http('.cache')

def process_image(url):
    response, content = h.request(url)
    image = Image.open(StringIO(content)) 
    return pytesseract.image_to_string(image), response.get('set-cookie')

def query_order(mailNum, checkCode, cookie):
    data = {'mailNum': mailNum, 'checkCode': checkCode}
    # because there are 2 set-cookie in the response of get_image
    # you cannot directly use response['set-cookie'] as request['Cookie']
    # Set-Cookie: JSESSIONID=C7LZWGGccR1h9lQChCGnVKPV9R01qFwfnQhpvRGNVpDsysx2pJ4F!-554346888; path=/; HttpOnly
    # Set-Cookie: BIGipServerweb_pool=168493834.40735.0000; path=/
    headers={'Cookie': cookie.replace(',', ';'),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*'}

    response, content = h.request('http://www.ems.com.cn/ems/order/singleQuery_t',
        'POST',
        urlencode(data),
        headers)

    return content

def scrape_html(content):
    tree = html.fromstring(content)
    list_delivery = tree.xpath('//table[@id="showTable"]/tr')
    s = ''

    for tr in list_delivery:
        for td in tr.itertext():
            s += td.strip() + ' '
        s += '\n'

    # strip here to handle the empty result
    s = s.strip()
    return s if s != '' else 'No delivery detail for this order!'
    

def retrieve_delivery_status(mailNum):
    url_ocr = 'http://www.ems.com.cn/ems/rand'

    checkCode, cookie = process_image(url_ocr)
    content = query_order(mailNum, checkCode, cookie)
    status = scrape_html(content)

    return status

#EA038500686NL
