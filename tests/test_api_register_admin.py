import json
from profileapp import create_app
import unittest


class FlaskTest(unittest.TestCase):

    def test_successful_register_admin(self):
        tester = create_app().test_client(self)

        response_profile = tester.post("/profiles/add/",
                                       data=json.dumps({'id': 0, 'description': 'admin'}),
                                       content_type='application/json')

        response = tester.post("/register_admin/",
                               data=json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com', 'password': '123456789',
                                                'national_id': '12345678', 'national_id_type': 'DNI',
                                                'alias': 'gonzalgo', 'profile': 0}),
                               content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['name'], "Gonza")
        self.assertEqual(data_back['email'], "algo@algo.com")
        self.assertEqual(data_back['alias'], "gonzalgo")
        self.assertEqual(data_back['id'], 1)
        self.assertEqual(status_code, 200)

    def test_register_admin_fails_user_not_admin(self):
        # Valid non-admin user gets a regular register as a non-admin and succeeds.
        # Similar non-admin valid user gets registered as an admin and fails.
        tester = create_app().test_client(self)

        response_profile = tester.post("/profiles/add/",
                                       data=json.dumps({'id': 0, 'description': 'admin'}),
                                       content_type='application/json')

        response_profile = tester.post("/profiles/add/",
                                       data=json.dumps({'id': 1, 'description': 'user'}),
                                       content_type='application/json')

        response_regular_register = tester.post("/register/",
                               data=json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com', 'password': '123456789',
                                                'national_id': '12345678', 'national_id_type': 'DNI',
                                                'alias': 'gonzalgo', 'profile': 1}),
                               content_type='application/json')

        response_admin_register = tester.post("/register_admin/",
                               data=json.dumps({'first_name': 'Jorge', 'last_name': 'Paez', 'email': 'algo2@algo.com', 'password': '123456789',
                                                'national_id': '123478', 'national_id_type': 'DNI',
                                                'alias': 'Jorgejo', 'profile': 1}),
                               content_type='application/json')

        status_code_regular = response_regular_register.status_code
        status_code_admin = response_admin_register.status_code
        data_back = json.loads(response_regular_register.get_data(as_text=True))
        self.assertEqual(data_back['name'], "Gonza")
        self.assertEqual(data_back['email'], "algo@algo.com")
        self.assertEqual(data_back['alias'], "gonzalgo")
        self.assertEqual(data_back['id'], 1)
        self.assertEqual(status_code_regular, 200)

        data_back_admin = json.loads(response_admin_register.get_data(as_text=True))
        self.assertEqual(data_back_admin['error'], "profile is not admin")
        self.assertEqual(status_code_admin, 400)
