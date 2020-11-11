import json
from profileapp import create_app
import unittest
from tests import VALID_PROFILE_ADMIN, VALID_ADMIN1_REGISTER, VALID_ADMIN1_LOGIN, VALID_USER2_REGISTER_WITH_ADMIN, \
    VALID_PROFILE_ANFITRION, VALID_ANFITRION1_REGISTER, VALID_ANFITRION1_LOGIN


class FlaskTest(unittest.TestCase):

    def test_login_user_insufficient_fields_one(self):
        tester = create_app().test_client(self)
        response = tester.post("/login/",
                               data=json.dumps({'email': 'Gonza'}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test_login_valid_user_fails_login_with_empty_password(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ADMIN,
                    content_type='application/json')

        tester.post("/register/",
                    data=VALID_ADMIN1_REGISTER,
                    content_type='application/json')

        response = tester.post("/login/",
                               data=json.dumps({'email': 'algo@algo.com', 'password': ''}),
                               content_type='application/json')

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['Error'], "User Password must not be empty")
        self.assertEqual(status_code, 400)

    def test_valid_user_login_successful(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ADMIN,
                    content_type='application/json')

        tester.post("/register/",
                    data=VALID_ADMIN1_REGISTER,
                    content_type='application/json')

        response = tester.post("/login/",
                               data=VALID_ADMIN1_LOGIN,
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
        self.assertEqual(data_back['Error'], "The email: algo@algo.com is not registered")
        self.assertEqual(status_code, 400)

    def test_login_unsuccessful_wrong_password(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ADMIN,
                    content_type='application/json')

        tester.post("/register/",
                    data=VALID_ADMIN1_REGISTER,
                    content_type='application/json')

        response = tester.post("/login/",
                               data=json.dumps({'email': 'algo@algo.com', 'password': 'otropassword'}),
                               content_type='application/json')

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['Error'], "User Password is invalid")
        self.assertEqual(status_code, 400)
