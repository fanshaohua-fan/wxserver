import pytesseract
from PIL import Image
from StringIO import StringIO
from urllib import urlencode
from lxml import html
import httplib2


httplib2.debuglevel = 0
h = httplib2.Http('.cache')

def process_image(url):
    response, content = h.request(url)
    image = Image.open(StringIO(content)) 
    return pytesseract.image_to_string(image), response.get('set-cookie')

def retrieve_delivery_status(mailNum):
    url_ocr = 'http://www.ems.com.cn/ems/rand'
    url_order_status = 'http://www.ems.com.cn/ems/order/singleQuery_t'

    checkCode, cookie = process_image(url_ocr)
    data = {'mailNum' : mailNum, 'checkCode' : checkCode}
    # because there are 2 set-cookie in the response of get_image
    # you cannot directly use response['set-cookie'] as request['Cookie']
    # Set-Cookie: JSESSIONID=C7LZWGGccR1h9lQChCGnVKPV9R01qFwfnQhpvRGNVpDsysx2pJ4F!-554346888; path=/; HttpOnly
    # Set-Cookie: BIGipServerweb_pool=168493834.40735.0000; path=/
    headers={'Cookie': cookie.replace(',', ';'), 'Content-Type':'application/x-www-form-urlencoded', 'Accept':'*/*'}

    response, content = h.request(url_order_status, 
        'POST',
        urlencode(data),
        headers)

    tree = html.fromstring(content)
    delivery = tree.xpath('//div[@id="s_div"]/table/tr/td/text()')

    for i, data in enumerate(delivery):
        delivery[i] = data.strip()

    s = ''
    for data in delivery:
        s += data + '\n'

    return s

#EA038500686NL
