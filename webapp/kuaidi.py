# -*- coding: utf-8 -*-
from urllib import urlencode
from lxml import html
import httplib2
import json


#httplib2.debuglevel = 1
h = httplib2.Http('.cache')

class kuaidi:
    name = None
    url = None
    orderno = None
    
class kuaidi_ems(kuaidi):
    def __init__(self, orderno):
        self.name = 'ems'
        self.url = 'http://www.ems.com.cn/ems/order/singleQuery_t'
        self.orderno = orderno

    def __format(self, content):
        tree = html.fromstring(content)
        delivery = tree.xpath('//table[@id="showTable"]/tr')
        status = ''

        for tr in delivery:
            for td in tr.itertext():
                status += td.strip() + ' '
            status += '\n'

        # strip here to handle the empty result
        status = status.strip()
        return status if status != '' else 'No delivery detail for this order!'

    def __ocr(self):
        data = {'url': 'http://www.ems.com.cn/ems/rand'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response, content = h.request('http://api:5000/ocr', 'POST', urlencode(data), headers)

        # {"cookie": "JSESSIONID=kgspS2HSqvD-QBf4ytuNJNG8Wp7E6Fg41QaA3sJZKK1jQq1ENZKZ!-999937407; path=/; HttpOnly; BIGipServerweb_pool=453706506.17695.0000; path=/", "msg": "OK", "result": "805341", "status": 200}
        j = json.loads(content)

        self.checkCode = j.get('result')
        self.Cookie = j.get('cookie')

    def status(self):
        #EA038500686NL
        self.__ocr()
        data = {'mailNum': self.orderno, 'checkCode': self.checkCode}
        headers={'Cookie': self.Cookie,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'}

        response, content = h.request(self.url, 'POST', urlencode(data), headers)

        return self.__format(content)

class kuaidi_oto(kuaidi):
    def __init__(self, orderno):
        self.name = 'otobv'
        # curl -v -H "Referer: http://www.otobv.com" "http://www.otobv.com/handle/order_track/search.ashx?expressnum=32588073216U8"
        self.url = 'http://www.otobv.com/handle/order_track/search.ashx?expressnum=%s'
        self.orderno = orderno

    def __format(self, content):
        status = ''

        c = json.loads(content)
        # ems status
        ems = c.get('obj').get('clist')
        if ems is not None and ems.has_key('data'):
            li = ems.get('data')
            for l in li:
                status += l.get('context') + '\n'
                status += l.get('time') + '\n'

        # oto status
        li = c.get('obj').get('list')
        for l in li:
            status += l.get('info') + '\n'
            status += l.get('createtime') + '\n'

        return status

    def status(self):
        headers={'Referer': 'http://www.otobv.com'}
        response, content = h.request(self.url % self.orderno, 'GET', None, headers)

        return self.__format(content)


