import json
from profileapp import create_app
import unittest


class FlaskTest(unittest.TestCase):

    def test_create_invalid_profile_one_not_enough_fields(self):
        tester = create_app().test_client(self)
        response = tester.post("/profile/add/",
                               data=json.dumps({'id': 0}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test_create_valid_profile(self):
        tester = create_app().test_client(self)
        response = tester.post("/profile/add/",
                               data=json.dumps({'id': 0, 'description': 'admin'}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
