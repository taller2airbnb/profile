import json
from profileapp import create_app
import unittest


class FlaskTest(unittest.TestCase):

    def test_create_profile_one_not_enough_fields(self):
        tester = create_app().test_client(self)
        response = tester.post("/profile/add/",
                               data=json.dumps({'id': 0}),
                               content_type='application/json')
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test_create_profile(self):
        tester = create_app().test_client(self)
        response = tester.post("/profile/add/",
                               data=json.dumps({'id': 0, 'description': 'admin'}),
                               content_type='application/json')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
