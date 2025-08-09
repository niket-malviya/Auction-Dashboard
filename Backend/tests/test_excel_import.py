import unittest
import json
import pandas as pd
from io import BytesIO
from app import create_app
from app.extensions import db
from models.user import User
from models.tournament import Tournament
from models.sport_type import SportType
from models.player import Player
import uuid
from werkzeug.security import generate_password_hash
from datetime import date

class ExcelImportTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create test user
            test_user = User(
                id=uuid.uuid4(),
                name='Test User',
                email='test@example.com',
                password=generate_password_hash('password123'),
                type='admin'
            )
            db.session.add(test_user)
            
            # Create sport type
            sport_type = SportType(
                id=uuid.uuid4(),
                sport_name='Cricket'
            )
            db.session.add(sport_type)
            
            # Create tournament
            tournament = Tournament(
                id=uuid.uuid4(),
                users_id=test_user.id,
                name='Test Tournament',
                sport_id=sport_type.id,
                tournament_type='League',
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 31),
                venue='Test Ground'
            )
            db.session.add(tournament)
            
            db.session.commit()
            
            self.test_user_id = str(test_user.id)
            self.tournament_id = str(tournament.id)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_excel_file(self):
        """Create a test Excel file with sample player data"""
        data = {
            'name': ['John', 'Jane', 'Mike'],
            'last_name': ['Doe', 'Smith', 'Johnson'],
            'flat_no': ['101', '102', '103'],
            'age': [25, 28, 30],
            'mobile_number': ['1234567890', '0987654321', '1122334455'],
            'bowler_type': ['right', 'left', 'right'],
            'batter_type': ['left', 'right', 'left'],
            'category': ['silver', 'gold', 'bronze'],
            'img_url': ['', '', '']
        }
        
        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        return output

    def test_download_template(self):
        """Test downloading Excel template"""
        # Login to get token
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
        
        # Test template download
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get('/excel-template', headers=headers)
        
        # Should return Excel file
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_import_players(self):
        """Test importing players from Excel"""
        # Login to get token
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
        
        # Create test Excel file
        excel_file = self.create_test_excel_file()
        
        # Test import
        headers = {'Authorization': f'Bearer {access_token}'}
        data = {'file': (excel_file, 'test_players.xlsx')}
        response = self.client.post(f'/tournament/{self.tournament_id}/import-players', 
                                  data=data,
                                  headers=headers,
                                  content_type='multipart/form-data')
        
        # Should return success
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('Successfully imported', response_data['message'])

    def test_import_without_auth(self):
        """Test import without authentication"""
        excel_file = self.create_test_excel_file()
        data = {'file': (excel_file, 'test_players.xlsx')}
        response = self.client.post(f'/tournament/{self.tournament_id}/import-players', 
                                  data=data,
                                  content_type='multipart/form-data')
        self.assertEqual(response.status_code, 401)

    def test_import_invalid_tournament(self):
        """Test import with invalid tournament ID"""
        # Login to get token
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        login_response = self.client.post('/login', 
                                        data=json.dumps(login_data),
                                        content_type='application/json')
        
        access_token = login_data['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Test with invalid tournament ID
        invalid_id = str(uuid.uuid4())
        excel_file = self.create_test_excel_file()
        data = {'file': (excel_file, 'test_players.xlsx')}
        response = self.client.post(f'/tournament/{invalid_id}/import-players', 
                                  data=data,
                                  headers=headers,
                                  content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main() 