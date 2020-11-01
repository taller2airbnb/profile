import json
from profileapp import create_app
import unittest


class FlaskTest(unittest.TestCase):

    def test__change_password_not_validated(self):
        tester = create_app().test_client(self)
        response = tester.post("/change_password/",
                               data=json.dumps({'validate': 'NO', 'email': 'asdasd@asd.com', 'new_pass': 'paez'}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test__change_password_unsuccessful_right_mail_empty_pass(self):
        tester = create_app().test_client(self)
        response_profile = tester.post("/profiles/add/",
                                       data=json.dumps({'id': 0, 'description': 'admin'}),
                                       content_type='application/json')

        response_user = tester.post("/register/",
                               data=json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com', 'password': '123456789',
                                                'national_id': '12345678', 'national_id_type': 'DNI',
                                                'alias': 'gonzalgo', 'profile': 0}),
                               content_type='application/json')
        response_password = tester.post("/change_password/",
                               data=json.dumps({'validate': 'OK', 'email': 'algo@algo.com', 'new_pass': ''}),
                               content_type='application/json')
        status_code = response_password.status_code
        self.assertEqual(status_code, 400)

    def test__change_password_unsuccessful_non_existent_email(self):
        tester = create_app().test_client(self)
        response = tester.post("/change_password/",
                               data=json.dumps({'validate': 'OK', 'email': 'asdasd@asd.com', 'new_pass': 'hello'}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test__fail_to_login_with_old_pass(self):
        tester = create_app().test_client(self)

        old_pass = '123456789'
        new_pass = 'tuvieja'

        response_profile = tester.post("/profiles/add/",
                                       data=json.dumps({'id': 0, 'description': 'admin'}),
                                       content_type='application/json')

        response_user = tester.post("/register/",
                               data=json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com', 'password': old_pass,
                                                'national_id': '12345678', 'national_id_type': 'DNI',
                                                'alias': 'gonzalgo', 'profile': 0}),
                               content_type='application/json')

        response_password = tester.post("/change_password/",
                               data=json.dumps({'validate': 'OK', 'email': 'algo@algo.com', 'new_pass': new_pass}),
                               content_type='application/json')

        response_login = tester.post("/login/",
                               data=json.dumps({'email': 'algo@algo.com', 'password': old_pass}),
                               content_type='application/json')

        status_code = response_password.status_code
        self.assertEqual(status_code, 200)

        data_back = json.loads(response_password.get_data(as_text=True))
        self.assertEqual(data_back['change_pass'], "OK")
        status_code = response_login.status_code
        self.assertEqual(status_code, 400)

    def test__change_password_successful(self):
        tester = create_app().test_client(self)

        old_pass = '123456789'
        new_pass = 'tuvieja'

        tester = create_app().test_client(self)
        response_profile = tester.post("/profiles/add/",
                                       data=json.dumps({'id': 0, 'description': 'admin'}),
                                       content_type='application/json')

        response_user = tester.post("/register/",
                               data=json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com', 'password': old_pass,
                                                'national_id': '12345678', 'national_id_type': 'DNI',
                                                'alias': 'gonzalgo', 'profile': 0}),
                               content_type='application/json')

        response_password = tester.post("/change_password/",
                               data=json.dumps({'validate': 'OK', 'email': 'algo@algo.com', 'new_pass': new_pass}),
                               content_type='application/json')

        response_login = tester.post("/login/",
                               data=json.dumps({'email': 'algo@algo.com', 'password': new_pass}),
                               content_type='application/json')

        status_code = response_password.status_code
        self.assertEqual(status_code, 200)

        data_back = json.loads(response_password.get_data(as_text=True))
        self.assertEqual(data_back['change_pass'], "OK")
        status_code = response_login.status_code
        self.assertEqual(status_code, 200)
