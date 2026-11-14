import unittest
from app import app


class TestAppSmoke(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    # Test that the application successfully loads
    def test_prediction_route_success(self):
        response = self.client.get('/')

        # Check that the application returns a successful response
        self.assertEqual(response.status_code, 200)

        # Check that the page contains content
        self.assertTrue(len(response.data) > 0)

    # Test that the weather input form is displayed
    def test_get_form(self):
        response = self.client.get('/')

        # Check that the form page loads successfully
        self.assertEqual(response.status_code, 200)

        # Check that the HTML contains a form
        self.assertIn(b'<form', response.data.lower())


if __name__ == '__main__':
    unittest.main()