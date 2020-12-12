import json
import config
from profileapp import create_app
import unittest
from tests import VALID_MODIFY_ANFITRION, INVALID_MODIFY_USER_EMPTY, INVALID_MODIFY_USER_BLANK, \
    VALID_MODIFY_ANFITRION_JUST_NAME, VALID_PROFILE_ADMIN, VALID_ADMIN1_REGISTER, VALID_PROFILE_ANFITRION, \
    VALID_ANFITRION1_REGISTER, VALID_ADMIN1_LOGIN, VALID_USER2_REGISTER_WITH_ADMIN, VALID_ANFITRION1_LOGIN, \
    VALID_PEPE_CHATRUC_BOOKBNB_REGISTER


class FlaskTest(unittest.TestCase):

    def test_successful_register_google(self):
        tester = create_app(config.TestingWithValidGoogle).test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ANFITRION,
                    content_type='application/json')

        response = tester.post("/user/",
                               data=json.dumps({'google_token': 'untokeeeen', 'user_type': 'googleuser', 'profile': 1}),
                               content_type='application/json')

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        print(data_back)
        self.assertEqual(data_back['id'], 1)
        self.assertEqual(status_code, 200)

    def test_fail_register_google_already_taken_mail(self):
        tester = create_app(config.TestingWithValidGoogle).test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ANFITRION,
                    content_type='application/json')

        tester.post("/user/",
                    data=json.dumps({'google_token': 'untokeeeen', 'user_type': 'googleuser', 'profile': 1}),
                    content_type='application/json')

        response = tester.post("/user/",
                               data=json.dumps({'google_token': 'untokeeeen', 'user_type': 'googleuser', 'profile': 1}),
                               content_type='application/json')

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['Error'], "Some User identifier is already taken: elpepechatruc@gmail.com or ")
        self.assertEqual(status_code, 403)

    def test_fail_register_invalid_google_token(self):
        tester = create_app(config.TestingWithInvalidGoogle).test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ANFITRION,
                    content_type='application/json')

        tester.post("/user/",
                    data=json.dumps({'google_token': 'untokeeeen', 'user_type': 'googleuser', 'profile': 1}),
                    content_type='application/json')

        response = tester.post("/user/",
                               data=json.dumps({'google_token': 'untokeeeen', 'user_type': 'googleuser', 'profile': 1}),
                               content_type='application/json')

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['Error'], "Not able to validate token with GoogleAPI")
        self.assertEqual(status_code, 401)

    def test_successful_register_login_google(self):
        tester = create_app(config.TestingWithValidGoogle).test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ANFITRION,
                    content_type='application/json')

        response = tester.post("/user/",
                               data=json.dumps({'google_token': 'untokeeeen', 'user_type': 'googleuser', 'profile': 1}),
                               content_type='application/json')

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['id'], 1)
        self.assertEqual(status_code, 200)

        response = tester.post("/login/",
                               data=json.dumps({'google_token': 'untokeeeen', 'user_type': 'googleuser', 'profile': 1}),
                               content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['id'], 1)
        self.assertEqual(status_code, 200)


    def test_unsuccessful_login_google_mail_taken_boonbnb_user(self):
        tester = create_app(config.TestingWithValidGoogle).test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ANFITRION,
                    content_type='application/json')

        response = tester.post("/user/",
                               data=VALID_PEPE_CHATRUC_BOOKBNB_REGISTER,
                               content_type='application/json')

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['id'], 1)
        self.assertEqual(status_code, 200)

        response = tester.post("/login/",
                               data=json.dumps({'google_token': 'untokeeeen', 'user_type': 'googleuser', 'profile': 1}),
                               content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['Error'], 'User register without Google Auth')
        self.assertEqual(status_code, 403)

    def test_google_user_cant_recover_password(self):
        tester = create_app(config.TestingWithValidGoogle).test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ANFITRION,
                    content_type='application/json')

        response = tester.post("/user/",
                               data=json.dumps({'google_token': 'untokeeeen', 'user_type': 'googleuser', 'profile': 1}),
                               content_type='application/json')

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['id'], 1)
        self.assertEqual(status_code, 200)

        response = tester.post("/recover_token/elpepechatruc@gmail.com")
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['Error'], 'User register with Google Auth cant recover password')
        self.assertEqual(status_code, 403)
