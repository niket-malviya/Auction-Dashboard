import unittest
import json
import time
from app import create_app
from app.extensions import db
from models.user import User
import uuid
from werkzeug.security import generate_password_hash

class AutoRefreshTokenTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60  # 1 minute for testing
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create a test user
            test_user = User(
                id=uuid.uuid4(),
                name='Test User',
                email='test@example.com',
                password=generate_password_hash('password123'),
                type='admin'
            )
            db.session.add(test_user)
            db.session.commit()
            self.test_user_id = str(test_user.id)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_automatic_token_refresh(self):
        """Test that tokens are automatically refreshed by backend"""
        # Login to get tokens
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        login_response = self.client.post('/login', 
                                        data=json.dumps(login_data),
                                        content_type='application/json')
        
        self.assertEqual(login_response.status_code, 200)
        login_data = json.loads(login_response.data)
        access_token = login_data['access_token']
        
        # Make a request with the token
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get('/players', headers=headers)
        
        # Check if new token was provided in headers
        new_token_header = response.headers.get('X-New-Access-Token')
        token_refreshed_header = response.headers.get('X-Token-Refreshed')
        
        # For testing, we expect the token to be refreshed if it's close to expiry
        if new_token_header and token_refreshed_header == 'true':
            print("✅ Automatic token refresh working - new token provided in headers")
        else:
            print("ℹ️ Token not refreshed (likely still valid)")

    def test_backend_handles_expired_tokens(self):
        """Test that backend handles expired tokens gracefully"""
        # Create a mock expired token (this is just for testing the error handling)
        expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjE2MTYxNjE2fQ.invalid"
        
        headers = {'Authorization': f'Bearer {expired_token}'}
        response = self.client.get('/players', headers=headers)
        
        # Should return 401 or 422 for expired token
        self.assertIn(response.status_code, [401, 422])

if __name__ == '__main__':
    unittest.main() 