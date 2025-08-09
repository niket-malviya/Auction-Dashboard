import unittest
import json
from app import create_app
from app.extensions import db
from models.user import User
import uuid

class RefreshTokenTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create a test user
            test_user = User(
                id=uuid.uuid4(),
                name='Test User',
                email='test@example.com',
                password='hashed_password',
                type='admin'
            )
            db.session.add(test_user)
            db.session.commit()
            self.test_user_id = str(test_user.id)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_returns_both_tokens(self):
        """Test that login returns both access and refresh tokens"""
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        response = self.client.post('/login', 
                                  data=json.dumps(login_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn('access_token', data)
        self.assertIn('refresh_token', data)
        self.assertIn('user', data)

    def test_refresh_token_works(self):
        """Test that refresh token can be used to get new access token"""
        # First login to get tokens
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        login_response = self.client.post('/login', 
                                        data=json.dumps(login_data),
                                        content_type='application/json')
        login_data = json.loads(login_response.data)
        refresh_token = login_data['refresh_token']
        
        # Use refresh token to get new access token
        headers = {'Authorization': f'Bearer {refresh_token}'}
        refresh_response = self.client.post('/refresh', headers=headers)
        
        self.assertEqual(refresh_response.status_code, 200)
        refresh_data = json.loads(refresh_response.data)
        
        self.assertIn('access_token', refresh_data)
        self.assertIn('user', refresh_data)

    def test_refresh_without_token_fails(self):
        """Test that refresh without token fails"""
        response = self.client.post('/refresh')
        self.assertEqual(response.status_code, 401)

    def test_refresh_with_invalid_token_fails(self):
        """Test that refresh with invalid token fails"""
        headers = {'Authorization': 'Bearer invalid_token'}
        response = self.client.post('/refresh', headers=headers)
        self.assertEqual(response.status_code, 422)

if __name__ == '__main__':
    unittest.main() 