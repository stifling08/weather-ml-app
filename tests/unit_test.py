
import unittest
from app import app, classify_weather, load_model, weather_classes
import numpy as np


class TestUnit(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    # Test proper handling of a missing input field
    def test_post_missing_field(self):
        form_data = {
            'temperature': '270.277',
            'pressure': '1006',
            'humidity': '84',
            # wind_speed is deliberately missing
            'wind_deg': '274',
            'rain_1h': '0',
            'rain_3h': '0',
            'snow': '0',
            'clouds': '9'
        }

        response = self.client.post('/', data=form_data)

        # Check that the application handles the missing field
        self.assertEqual(response.status_code, 200)

        # Check that an error message is displayed
        self.assertIn(b'Error processing input', response.data)

    # Test that the trained weather model loads correctly
    def test_model_can_be_loaded(self):
        model = load_model()

        # Check that a model has been returned
        self.assertIsNotNone(model)

        # Check that the model supports predictions
        self.assertTrue(hasattr(model, 'predict'))

    # Test that clear weather is classified within the valid classes
    def test_clear_classification_output(self):
        test_input = np.array(
            [[269.686, 1002, 78, 0, 23, 0, 0, 0, 0]]
        )

        class_result, latency = classify_weather(test_input)

        self.assertIn(class_result, weather_classes)
        self.assertIsInstance(latency, (int, float))
        self.assertGreaterEqual(latency, 0)

    # Test that rainy weather is classified within the valid classes
    def test_rainy_classification_output(self):
        test_input = np.array(
            [[279.626, 998, 99.1, 314, 0, 3, 0, 0, 88]]
        )

        class_result, latency = classify_weather(test_input)

        self.assertIn(class_result, weather_classes)
        self.assertIsInstance(latency, (int, float))
        self.assertGreaterEqual(latency, 0)

    # Test that foggy weather is classified within the valid classes
    def test_foggy_classification_output(self):
        test_input = np.array(
            [[289.47, 1015, 88.2, 300, 0, 0, 0, 0, 20]]
        )

        class_result, latency = classify_weather(test_input)

        self.assertIn(class_result, weather_classes)
        self.assertIsInstance(latency, (int, float))
        self.assertGreaterEqual(latency, 0)


if __name__ == '__main__':
    unittest.main()
