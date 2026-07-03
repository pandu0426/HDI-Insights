import unittest
import json
import numpy as np
from app import app, BOUNDS

class TestHDIPredictionSystem(unittest.TestCase):
    
    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_page(self):
        """Verify the home page loads successfully and contains the correct elements."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html_content = response.data.decode('utf-8')
        self.assertIn("HDI Insight AI", html_content)
        self.assertIn("id=\"hdi-predict-form\"", html_content)

    def test_prediction_success(self):
        """Verify prediction endpoint returns expected JSON format and valid prediction scores."""
        payload = {
            'Life_Expectancy': 75.5,
            'Expected_Schooling': 14.2,
            'Mean_Schooling': 10.5,
            'GNI_Per_Capita': 25000.0
        }
        response = self.client.post(
            '/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data['success'])
        self.assertIn('prediction', data)
        self.assertIn('category', data)
        self.assertIn('confidence', data)
        self.assertIn('explanation', data)
        
        hdi = data['prediction']
        self.assertTrue(0.0 <= hdi <= 1.0)

    def test_prediction_validation_failures(self):
        """Verify that out-of-bounds parameters are correctly validated and rejected."""
        # 1. Test missing field
        payload_missing = {
            'Life_Expectancy': 75.5,
            'Expected_Schooling': 14.2,
            'Mean_Schooling': 10.5
            # GNI_Per_Capita is missing
        }
        response = self.client.post(
            '/predict',
            data=json.dumps(payload_missing),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertFalse(data['success'])
        self.assertIn('GNI_Per_Capita', data['errors'])

        # 2. Test values way out of bounds
        payload_out_of_bounds = {
            'Life_Expectancy': 15.0, # Below min (20.0)
            'Expected_Schooling': 25.0, # Above max (22.0)
            'Mean_Schooling': -1.0, # Below min (0.0)
            'GNI_Per_Capita': 200000.0 # Above max (150000.0)
        }
        response = self.client.post(
            '/predict',
            data=json.dumps(payload_out_of_bounds),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertFalse(data['success'])
        self.assertIn('Life_Expectancy', data['errors'])
        self.assertIn('Expected_Schooling', data['errors'])
        self.assertIn('Mean_Schooling', data['errors'])
        self.assertIn('GNI_Per_Capita', data['errors'])

    def test_prediction_boundary_edges(self):
        """Verify prediction behavior at boundary extrema (Min and Max)."""
        # Test minimum limits
        payload_min = {
            'Life_Expectancy': BOUNDS['Life_Expectancy']['min'],
            'Expected_Schooling': BOUNDS['Expected_Schooling']['min'],
            'Mean_Schooling': BOUNDS['Mean_Schooling']['min'],
            'GNI_Per_Capita': BOUNDS['GNI_Per_Capita']['min']
        }
        response_min = self.client.post(
            '/predict',
            data=json.dumps(payload_min),
            content_type='application/json'
        )
        self.assertEqual(response_min.status_code, 200)
        data_min = json.loads(response_min.data.decode('utf-8'))
        self.assertTrue(0.0 <= data_min['prediction'] <= 1.0)
        self.assertEqual(data_min['category'], 'Low')

        # Test maximum limits
        payload_max = {
            'Life_Expectancy': BOUNDS['Life_Expectancy']['max'],
            'Expected_Schooling': BOUNDS['Expected_Schooling']['max'],
            'Mean_Schooling': BOUNDS['Mean_Schooling']['max'],
            'GNI_Per_Capita': BOUNDS['GNI_Per_Capita']['max']
        }
        response_max = self.client.post(
            '/predict',
            data=json.dumps(payload_max),
            content_type='application/json'
        )
        self.assertEqual(response_max.status_code, 200)
        data_max = json.loads(response_max.data.decode('utf-8'))
        self.assertTrue(0.0 <= data_max['prediction'] <= 1.0)
        self.assertEqual(data_max['category'], 'Very High')

if __name__ == '__main__':
    unittest.main()
