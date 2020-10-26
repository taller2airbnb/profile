from profileapp import create_app
import unittest


class FlaskTest(unittest.TestCase):

    # Check for response 200
    def test_index(self):
        app = create_app()

        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Check for response 200
    def test_health(self):
        app = create_app()

        tester = app.test_client(self)
        response = tester.get("/health")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)


if __name__ == '__main__':
    unittest.main()
