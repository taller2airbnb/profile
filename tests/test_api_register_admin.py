import json
from profileapp import create_app
import unittest
from tests import VALID_PROFILE_ADMIN, VALID_ADMIN1_REGISTER, VALID_ADMIN1_LOGIN, VALID_USER2_REGISTER_WITH_ADMIN, \
    VALID_PROFILE_ANFITRION, VALID_ANFITRION1_REGISTER, VALID_ANFITRION1_LOGIN


class FlaskTest(unittest.TestCase):

    def test_successful_register_admin(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ADMIN,
                    content_type='application/json')

        tester.post("/user/",
                    data=VALID_ADMIN1_REGISTER,
                    content_type='application/json')

        tester.post("/login/",
                    data=VALID_ADMIN1_LOGIN,
                    content_type='application/json')

        response = tester.post("/register_admin/",
                               data=VALID_USER2_REGISTER_WITH_ADMIN,
                               content_type='application/json')

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['name'], "Admin")
        self.assertEqual(data_back['email'], "admin@algo.com")
        self.assertEqual(data_back['alias'], "administrador")
        self.assertEqual(data_back['id'], 2)
        self.assertEqual(status_code, 200)

    def test_register_admin_fails_user_not_admin(self):
        # Login with anfitrion and try to create admin must fail
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ANFITRION,
                    content_type='application/json')

        tester.post("/user/",
                    data=VALID_ANFITRION1_REGISTER,
                    content_type='application/json')

        tester.post("/login/",
                    data=VALID_ANFITRION1_LOGIN,
                    content_type='application/json')

        response = tester.post("/register_admin/",
                               data=json.dumps({'first_name': 'Jorge', 'last_name': 'Paez', 'email': 'algo2@algo.com', 'password': '123456789',
                                                'national_id': '123478', 'national_id_type': 'DNI',
                                                'alias': 'Jorgejo', 'user_logged_id': 1}),
                               content_type='application/json')

        status_code = response.status_code
        data_back_admin = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back_admin['Error'], "The User: 1 is not an admin")
        self.assertEqual(status_code, 400)
