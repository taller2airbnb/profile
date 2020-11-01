import json
from profileapp import create_app
import unittest


class FlaskTest(unittest.TestCase):

    def test_login_user_insufficient_fields_one(self):
        tester = create_app().test_client(self)
        response = tester.post("/login/",
                               data=json.dumps({'email': 'Gonza'}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test_login_user_with_empty_password(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=json.dumps({'id': 0, 'description': 'admin'}),
                    content_type='application/json')

        tester.post("/register/",
                    data=json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com', 'password': '',
                                     'national_id': '12345678', 'national_id_type': 'DNI',
                                     'alias': 'gonzalgo', 'profile': 0}),
                    content_type='application/json')

        response = tester.post("/login/",
                               data=json.dumps({'email': 'algo@algo.com', 'password': ''}),
                               content_type='application/json')

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['error'], "password is empty")
        self.assertEqual(status_code, 400)

    def test_login_successful(self):
        tester = create_app().test_client(self)

        response_profile = tester.post("/profiles/add/",
                                       data=json.dumps({'id': 0, 'description': 'admin'}),
                                       content_type='application/json')

        tester.post("/register/",
                               data=json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com', 'password': '123456789',
                                                'national_id': '12345678', 'national_id_type': 'DNI',
                                                'alias': 'gonzalgo', 'profile': 0}),
                               content_type='application/json')

        response = tester.post("/login/",
                               data=json.dumps({'email': 'algo@algo.com', 'password': '123456789'}),
                               content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['name'], "Gonza")
        self.assertEqual(data_back['email'], "algo@algo.com")
        self.assertEqual(data_back['alias'], "gonzalgo")
        self.assertEqual(data_back['id'], 1)
        self.assertEqual(status_code, 200)

    def test_login_unsuccessful_user_non_existent(self):
        tester = create_app().test_client(self)

        response = tester.post("/login/",
                               data=json.dumps({'email': 'algo@algo.com', 'password': '123456789'}),
                               content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['error'], "user not existent")
        self.assertEqual(status_code, 400)

    def test_login_unsuccessful_wrong_password(self):
        tester = create_app().test_client(self)

        response_profile = tester.post("/profiles/add/",
                                       data=json.dumps({'id': 0, 'description': 'admin'}),
                                       content_type='application/json')

        tester.post("/register/",
                               data=json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com', 'password': '123456789',
                                                'national_id': '12345678', 'national_id_type': 'DNI',
                                                'alias': 'gonzalgo', 'profile': 0}),
                               content_type='application/json')

        response = tester.post("/login/",
                               data=json.dumps({'email': 'algo@algo.com', 'password': 'otropassword'}),
                               content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['error'], "login failed")
        self.assertEqual(status_code, 400)