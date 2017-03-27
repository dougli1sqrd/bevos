import unittest

from bevos import ghapi

class TestGhApi(unittest.TestCase):

    def test_make_release_data(self):
        data = ghapi.make_release_data("v1.2.3", "master", "foo", True)
        expected = {
            "tag_name": "v1.2.3",
            "target_commitish": "master",
            "name": "v1.2.3",
            "body": "foo",
            "draft": True,
            "prerelease": False
        }
        self.assertEqual(expected, data)

    def test_make_release_endpoint(self):
        endpoint = ghapi.make_release_endpoint("Obama", "aca")
        self.assertEqual("/repos/Obama/aca/releases", endpoint)

    def test_endpoint_url(self):
        url = ghapi.endpoint_url("https://github.com", "/repos/Obama/aca/releases")
        self.assertEqual("https://github.com/repos/Obama/aca/releases", url)



if __name__ == '__main__':
    unittest.main()
