import unittest
import re
from webapp import ocr

class TestOCR(unittest.TestCase):

    def test_process_image(self):
        url = 'http://www.ems.com.cn/ems/rand'
        d = ocr.process_image(url)

        self.assertTrue(re.match('\d{6}', d[0]))
        self.assertTrue(isinstance(d[1], str))

    def test_retrieve_delivery_status(self):
        mail = 'EA038500686NL'
        d = ocr.retrieve_delivery_status(mail)

        self.assertTrue(d)

    def test_retrieve_delivery_status_invalid(self):
        mail = 'EA03850068NL'
        d = ocr.retrieve_delivery_status(mail)

        self.assertEqual(d, 'No delivery detail for this order!')

if __name__ == '__main__':
    unittest.main()
