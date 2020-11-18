import json
from profileapp import create_app
import unittest
from tests import VALID_MODIFY_ANFITRION, INVALID_MODIFY_USER_EMPTY, INVALID_MODIFY_USER_BLANK, VALID_USER_INFO, \
    VALID_MODIFY_ANFITRION_JUST_NAME, VALID_PROFILE_ADMIN, VALID_ADMIN1_REGISTER, VALID_PROFILE_ANFITRION, \
    VALID_ANFITRION1_REGISTER


class FlaskTest(unittest.TestCase):
    class FlaskTest(unittest.TestCase):

        def test_create_user_insufficient_fields_one(self):
            tester = create_app().test_client(self)
            response = tester.post("/user/",
                                   data=json.dumps({'first_name': 'Gonza'}),
                                   content_type='application/json')
            status_code = response.status_code
            self.assertEqual(status_code, 400)

        def test_create_user_insufficient_fields_multiple(self):
            tester = create_app().test_client(self)
            response = tester.post("/user/",
                                   data=json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'mail': 'algo@algo.com',
                                                    'national_id': '12345678',
                                                    'national_id_type': 'DNI', 'password': '123456789'}),
                                   content_type='application/json')
            status_code = response.status_code
            self.assertEqual(status_code, 400)

        def test_create_user_sufficient_fields_non_existent_profile(self):
            tester = create_app().test_client(self)
            response = tester.post("/user/",
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

            tester.post("/user/",
                        data=VALID_ANFITRION1_REGISTER,
                        content_type='application/json')

            response = tester.post("/user/",
                                   data=json.dumps(
                                       {'first_name': 'Jorge', 'last_name': 'Paez', 'email': 'anfi@algo.com',
                                        'password': '123456789', 'national_id': '123478',
                                        'national_id_type': 'DNI', 'alias': 'Jorgejo', 'user_logged_id': 1,
                                        'profile': 1}),
                                   content_type='application/json')

            status_code = response.status_code
            data_back_admin = json.loads(response.get_data(as_text=True))
            self.assertEqual(data_back_admin['Error'],
                             "Some User identifier is already taken: anfi@algo.com or Jorgejo")
            self.assertEqual(status_code, 400)

        def test_register_fails_user_alias_taken(self):
            tester = create_app().test_client(self)

            tester.post("/profiles/add/",
                        data=VALID_PROFILE_ANFITRION,
                        content_type='application/json')

            tester.post("/user/",
                        data=VALID_ANFITRION1_REGISTER,
                        content_type='application/json')

            response = tester.post("/user/",
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

            response = tester.post("/user/",
                                   data=json.dumps(
                                       {'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com',
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

            response = tester.post("/user/",
                                   data=VALID_ADMIN1_REGISTER,
                                   content_type='application/json')
            status_code = response.status_code
            data_back = json.loads(response.get_data(as_text=True))
            self.assertEqual(data_back['name'], "Gonza")
            self.assertEqual(data_back['email'], "algo@algo.com")
            self.assertEqual(data_back['alias'], "gonzalgo")
            self.assertEqual(data_back['id'], 1)
            self.assertEqual(status_code, 200)

    def test__modify_fields_for_non_existent_user(self):
        tester = create_app().test_client(self)

        response = tester.put("/user/",
                              data=VALID_MODIFY_ANFITRION,
                              content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['Error'], "Not exists User: " + str(json.loads(VALID_MODIFY_ANFITRION)['id']))
        self.assertEqual(status_code, 400)

    def test_modify_fields_empty_non_mandatory_fields(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ADMIN,
                    content_type='application/json')

        tester.post("/user/",
                    data=VALID_ADMIN1_REGISTER,
                    content_type='application/json')

        response = tester.put("/user/",
                              data=INVALID_MODIFY_USER_EMPTY,
                              content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['Error'], 'No fields were submitted in the request to modify user.')
        self.assertEqual(status_code, 400)

        response = tester.put("/user/",
                              data=INVALID_MODIFY_USER_BLANK,
                              content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['Error'], 'No fields were submitted in the request to modify user.')
        self.assertEqual(status_code, 400)

    def test_get_user_info_successfully(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ADMIN,
                    content_type='application/json')

        tester.post("/user/",
                    data=VALID_ADMIN1_REGISTER,
                    content_type='application/json')

        response = tester.get("/user/1")

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        test_user = json.loads(VALID_ADMIN1_REGISTER)

        self.assertEqual(data_back['first_name'], test_user['first_name'])
        self.assertEqual(data_back['last_name'], test_user['last_name'])
        self.assertEqual(data_back['national_id'], test_user['national_id'])
        self.assertEqual(data_back['national_id_type'], test_user['national_id_type'])
        self.assertEqual(data_back['email'], test_user['email'])
        self.assertEqual(data_back['alias'], test_user['alias'])
        self.assertEqual(status_code, 200)

    def test_modify_user_info_successfully(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ADMIN,
                    content_type='application/json')

        tester.post("/user/",
                    data=VALID_ADMIN1_REGISTER,
                    content_type='application/json')

        response = tester.get("/user/1")

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        test_user = json.loads(VALID_ADMIN1_REGISTER)

        self.assertEqual(data_back['first_name'], test_user['first_name'])
        self.assertEqual(data_back['last_name'], test_user['last_name'])
        self.assertEqual(data_back['national_id'], test_user['national_id'])
        self.assertEqual(data_back['national_id_type'], test_user['national_id_type'])
        self.assertEqual(data_back['email'], test_user['email'])
        self.assertEqual(data_back['alias'], test_user['alias'])
        self.assertEqual(status_code, 200)

        tester.put("/user/",
                   data=VALID_MODIFY_ANFITRION,
                   content_type='application/json')

        response = tester.get("/user/1")

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        modified_values = json.loads(VALID_MODIFY_ANFITRION)

        self.assertEqual(data_back['first_name'], modified_values['first_name'])
        self.assertEqual(data_back['last_name'], modified_values['last_name'])
        self.assertEqual(data_back['national_id'], modified_values['national_id'])
        self.assertEqual(data_back['national_id_type'], modified_values['national_id_type'])
        self.assertEqual(data_back['email'], test_user['email'])
        self.assertEqual(data_back['alias'], test_user['alias'])
        self.assertEqual(status_code, 200)

    def test_modify_user_info_successfully_just_name(self):
        tester = create_app().test_client(self)

        tester.post("/profiles/add/",
                    data=VALID_PROFILE_ADMIN,
                    content_type='application/json')

        tester.post("/user/",
                    data=VALID_ADMIN1_REGISTER,
                    content_type='application/json')

        response = tester.get("/user/1")

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        test_user = json.loads(VALID_ADMIN1_REGISTER)

        self.assertEqual(data_back['first_name'], test_user['first_name'])
        self.assertEqual(data_back['last_name'], test_user['last_name'])
        self.assertEqual(data_back['national_id'], test_user['national_id'])
        self.assertEqual(data_back['national_id_type'], test_user['national_id_type'])
        self.assertEqual(data_back['email'], test_user['email'])
        self.assertEqual(data_back['alias'], test_user['alias'])
        self.assertEqual(status_code, 200)

        tester.put("/user/",
                   data=VALID_MODIFY_ANFITRION_JUST_NAME,
                   content_type='application/json')

        response = tester.get("/user/1")

        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        modified_values = json.loads(VALID_MODIFY_ANFITRION_JUST_NAME)

        self.assertEqual(data_back['first_name'], modified_values['first_name'])
        self.assertEqual(data_back['last_name'], test_user['last_name'])
        self.assertEqual(data_back['national_id'], test_user['national_id'])
        self.assertEqual(data_back['national_id_type'], test_user['national_id_type'])
        self.assertEqual(data_back['email'], test_user['email'])
        self.assertEqual(data_back['alias'], test_user['alias'])
        self.assertEqual(status_code, 200)
