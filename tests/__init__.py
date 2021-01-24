from unittest import TestCase

from flask.ext.dummyimage import _get_size


class SizeTest(TestCase):
    def test_get_size(self):
        self.assertEqual((200, 200), _get_size("200"))
        self.assertEqual((640, 480), _get_size("640x480"))
