import json
from profileapp import create_app
import unittest


class FlaskTest(unittest.TestCase):

    def test_create_invalid_profile_one_not_enough_fields(self):
        tester = create_app().test_client(self)
        response = tester.post("/profiles/add/",
                               data=json.dumps({'id': 0}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test_create_valid_profile(self):
        tester = create_app().test_client(self)
        response = tester.post("/profiles/add/",
                               data=json.dumps({'id': 0, 'description': 'admin'}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_create_and_get_profiles(self):
        tester = create_app().test_client(self)
        tester.post("/profiles/add/",
                               data=json.dumps({'id': 0, 'description': 'admin'}),
                               content_type='application/json')
        tester.post("/profiles/add/",
                               data=json.dumps({'id': 1, 'description': 'anfitrion'}),
                               content_type='application/json')
        response = tester.get("/profiles/")
        status_code = response.status_code
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['data']['profiles'][0]['id'], 0)
        self.assertEqual(data['data']['profiles'][0]['description'], 'admin')
        self.assertEqual(data['data']['profiles'][1]['id'], 1)
        self.assertEqual(data['data']['profiles'][1]['description'], 'anfitrion')
        self.assertEqual(data['status'], 'success')
        self.assertEqual(status_code, 200)
