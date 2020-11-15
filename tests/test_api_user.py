import json
from profileapp import create_app
import unittest
from tests import VALID_MODIFY_ANFITRION, VALID_PROFILE_ADMIN, VALID_ADMIN1_REGISTER, INVALID_MODIFY_USER_EMPTY, \
    INVALID_MODIFY_USER_BLANK, VALID_USER_INFO, VALID_MODIFY_ANFITRION_JUST_NAME


class FlaskTest(unittest.TestCase):

    def test__modify_fields_for_non_existent_user(self):
        tester = create_app().test_client(self)

        response = tester.post("/user/modify/",
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

        tester.post("/register/",
                    data=VALID_ADMIN1_REGISTER,
                    content_type='application/json')

        response = tester.post("/user/modify/",
                               data=INVALID_MODIFY_USER_EMPTY,
                               content_type='application/json')
        status_code = response.status_code
        data_back = json.loads(response.get_data(as_text=True))
        self.assertEqual(data_back['Error'], 'No fields were submitted in the request to modify user.')
        self.assertEqual(status_code, 400)

        response = tester.post("/user/modify/",
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

        tester.post("/register/",
                    data=VALID_ADMIN1_REGISTER,
                    content_type='application/json')

        response = tester.get("/user/data/",
                              data=VALID_USER_INFO,
                              content_type='application/json')
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

        tester.post("/register/",
                    data=VALID_ADMIN1_REGISTER,
                    content_type='application/json')

        response = tester.get("/user/data/",
                              data=VALID_USER_INFO,
                              content_type='application/json')
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

        tester.post("/user/modify/",
                    data=VALID_MODIFY_ANFITRION,
                    content_type='application/json')

        response = tester.get("/user/data/",
                              data=VALID_USER_INFO,
                              content_type='application/json')
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

        tester.post("/register/",
                    data=VALID_ADMIN1_REGISTER,
                    content_type='application/json')

        response = tester.get("/user/data/",
                              data=VALID_USER_INFO,
                              content_type='application/json')
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

        tester.post("/user/modify/",
                    data=VALID_MODIFY_ANFITRION_JUST_NAME,
                    content_type='application/json')

        response = tester.get("/user/data/",
                              data=VALID_USER_INFO,
                              content_type='application/json')
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
