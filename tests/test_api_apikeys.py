import json
from profileapp import create_app
import unittest


class FlaskTest(unittest.TestCase):

    def test_create_valid_apikey(self):
        tester = create_app().test_client(self)
        response = tester.post("/apikey/add/",
                               data=json.dumps({'name_from': 'Alguien'}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_create_and_get_apikeys(self):
        tester = create_app().test_client(self)
        response = tester.post("/apikey/add/",
                               data=json.dumps({'name_from': 'Alguien'}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        response = tester.get("/apikey/")
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['apikeys'][2]['name_from'], 'Alguien')
        self.assertEqual(status_code, 200)

    def test_create_and_change_active_status_apikeys(self):
        tester = create_app().test_client(self)
        response = tester.post("/apikey/add/",
                               data=json.dumps({'name_from': 'Alguien'}),
                               content_type='application/json')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        response = tester.get("/apikey/")
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['apikeys'][2]['name_from'], 'Alguien')
        self.assertEqual(status_code, 200)
        response = tester.put("/apikey/3/active_status",
                              data=json.dumps({'active': False}),
                              content_type='application/json')
        response = tester.get("/apikey/")
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['apikeys'][2]['active'], False)
