import json
from profileapp import create_app
import unittest


class FlaskTest(unittest.TestCase):

    def test_create_user_one_not_enough_fields(self):
        tester = create_app().test_client(self)
        response = tester.post("/register/",
                               data=json.dumps({'name': 'Gonza'}),
                               content_type='application/json')
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test_create_user_various_not_enough_fields(self):
        tester = create_app().test_client(self)
        response = tester.post("/register/",
                               data=json.dumps({'name': 'Gonza', 'mail': 'algo@algo.com', 'national_id': '12345678',
                                                'national_id_type': 'DNI', 'password': '123456789'}),
                               content_type='application/json')
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test_create_user_enough_fields_non_existent_profile(self):
        tester = create_app().test_client(self)
        response = tester.post("/register/",
                               data=json.dumps({'name': 'Gonza', 'email': 'algo@algo.com', 'password': '123456789',
                                                'national_id': '12345678', 'national_id_type': 'DNI',
                                                'alias': 'gonzalgo', 'profile': 9}),
                               content_type='application/json')
        statuscode = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['error'], "non existent profile")
        self.assertEqual(statuscode, 400)

    def test_create_user_enough_fields_existent_profile(self):
        tester = create_app().test_client(self)

        response_profile = tester.post("/profile/add/",
                    data=json.dumps({'id': 0, 'description': 'admin'}),
                    content_type='application/json')

        response = tester.post("/register/",
                               data=json.dumps({'name': 'Gonza', 'email': 'algo@algo.com', 'password': '123456789',
                                                'national_id': '12345678', 'national_id_type': 'DNI',
                                                'alias': 'gonzalgo', 'profile': 0}),
                               content_type='application/json')
        statuscode = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['name'], "Gonza")
        self.assertEqual(data_back['email'], "algo@algo.com")
        self.assertEqual(data_back['alias'], "gonzalgo")
        self.assertEqual(data_back['id'], 1)
        self.assertEqual(statuscode, 200)
