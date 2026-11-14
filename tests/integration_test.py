
import unittest
import re
from app import app


class TestModelAppIntegration(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    # Test that weather information is submitted successfully
    # and processed by the trained machine learning model
    def test_model_app_integration(self):

        form_data = {
            'temperature': '275.15',
            'pressure': '1013',
            'humidity': '85',
            'wind_speed': '3.6',
            'wind_deg': '180',
            'rain_1h': '0',
            'rain_3h': '0',
            'snow': '0',
            'clouds': '20'
        }

        # Submit weather information to the Flask application
        response = self.client.post('/', data=form_data)

        html_text = response.data.decode('utf-8').lower()

        # Check that the application responds successfully
        self.assertEqual(response.status_code, 200)

        # Check that the results page displays a weather prediction
        valid_classes = [
            'clear', 'cloudy', 'drizzly', 'foggy', 'hazey',
            'misty', 'rainy', 'smokey', 'thunderstorm'
        ]

        prediction_found = re.search(
            r'the weather is:</strong>\s*(' +
            '|'.join(valid_classes) + r')\b',
            html_text
        )

        self.assertIsNotNone(
            prediction_found,
            "A valid weather prediction was not displayed."
        )

        # Check that the prediction processing time is displayed
        self.assertRegex(
            html_text,
            r'prediction time:</strong>\s*\d+(?:\.\d+)?\s*ms'
        )


if __name__ == '__main__':
    unittest.main()
