import unittest
import json
from Captcha import Captcha


class TestOCR(unittest.TestCase):

    def test_ocr(self):
        url = 'http://www.ems.com.cn/ems/rand'
        captcha = Captcha(url)
        captcha.ocr()

        self.assertTrue(captcha.status, 200)

    def test_json(self):
        url = 'http://www.ems.com.cn/ems/rand'
        captcha = Captcha(url)
        captcha.ocr()

        response = json.loads(captcha.json())

        self.assertTrue(response.get('status'), 200)


if __name__ == '__main__':
    unittest.main()
