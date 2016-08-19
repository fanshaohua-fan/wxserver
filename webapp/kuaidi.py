# -*- coding: utf-8 -*-
import httplib2
import json


httplib2.debuglevel = 1
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
        if ems.has_key('data'):
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


