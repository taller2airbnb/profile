import json
from profileapp import create_app
import unittest
from tests import VALID_PROFILE_ADMIN, VALID_ADMIN1_REGISTER, VALID_PROFILE_ANFITRION, VALID_ANFITRION1_REGISTER


class FlaskTest(unittest.TestCase):

    def test_create_user_insufficient_fields_one(self):
        tester = create_app().test_client(self)
        response = tester.post("/register/",
                               data=json.dumps({'first_name': 'Gonza'}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test_create_user_insufficient_fields_multiple(self):
        tester = create_app().test_client(self)
        response = tester.post("/register/",
                               data=json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'mail': 'algo@algo.com',
                                                'national_id': '12345678',
                                                'national_id_type': 'DNI', 'password': '123456789'}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test_create_user_sufficient_fields_non_existent_profile(self):
        tester = create_app().test_client(self)
        response = tester.post("/register/",
                               data=VALID_ADMIN1_REGISTER,
                               content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['Error'], "Not exists Profile by id: 0")
        self.assertEqual(status_code, 400)

    def test_register_fails_user_email_taken(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ANFITRION,
                    content_type='application/json')

        tester.post("/register/",
                    data=VALID_ANFITRION1_REGISTER,
                    content_type='application/json')

        response = tester.post("/register/",
                               data=json.dumps({'first_name': 'Jorge', 'last_name': 'Paez', 'email': 'anfi@algo.com',
                                                'password': '123456789', 'national_id': '123478',
                                                'national_id_type': 'DNI', 'alias': 'Jorgejo', 'user_logged_id': 1,
                                                'profile': 1}),
                               content_type='application/json')

        status_code = response.status_code
        data_back_admin = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back_admin['Error'], "Some User identifier is already taken: anfi@algo.com or Jorgejo")
        self.assertEqual(status_code, 400)

    def test_register_fails_user_alias_taken(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ANFITRION,
                    content_type='application/json')

        tester.post("/register/",
                    data=VALID_ANFITRION1_REGISTER,
                    content_type='application/json')

        response = tester.post("/register/",
                               data=json.dumps(
                                   {'first_name': 'Jorge', 'last_name': 'Paez', 'email': 'algo2@algo.com',
                                    'password': '123456789', 'national_id': '123478',
                                    'national_id_type': 'DNI', 'alias': 'anfitrion', 'user_logged_id': 1,
                                    'profile': 1}),
                               content_type='application/json')

        status_code = response.status_code
        data_back_admin = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back_admin['Error'],
                         "Some User identifier is already taken: algo2@algo.com or anfitrion")
        self.assertEqual(status_code, 400)

    def test_create_user_with_empty_password(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ADMIN,
                    content_type='application/json')

        response = tester.post("/register/",
                               data=json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com',
                                                'password': '', 'national_id': '12345678', 'national_id_type': 'DNI',
                                                'alias': 'gonzalgo', 'profile': 0}),
                               content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['Error'], "User Password must not be empty")
        self.assertEqual(status_code, 400)

    def test_create_user_successful_sufficient_fields_existent_profile(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ADMIN,
                    content_type='application/json')

        response = tester.post("/register/",
                               data=VALID_ADMIN1_REGISTER,
                               content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['name'], "Gonza")
        self.assertEqual(data_back['email'], "algo@algo.com")
        self.assertEqual(data_back['alias'], "gonzalgo")
        self.assertEqual(data_back['id'], 1)
        self.assertEqual(status_code, 200)
