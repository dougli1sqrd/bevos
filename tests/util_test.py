import io
import unittest
from unittest import mock

from bevos import util

class TestFileContext(unittest.TestCase):

    def test_util_context_success(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="hello world")) as mock_open:
            with util.FileContext("/some/path", "r") as result:
                self.assertEqual(result.file.read(), "hello world")


    def test_util_context_closes_file(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="hello world")) as mock_open:
            with util.FileContext("/some/path", "r") as result:
                pass
                
            result.file.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
