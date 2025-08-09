import unittest
import json
from app import create_app
from app.extensions import db
from models.user import User
from models.tournament import Tournament
from models.sport_type import SportType
from models.team import Team
from models.player import Player
from models.team_player import TeamPlayer
import uuid
from werkzeug.security import generate_password_hash
from datetime import date

class PDFExportTestCase(unittest.TestCase):
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
            
            # Create team
            team = Team(
                id=uuid.uuid4(),
                team_name='Test Team',
                owner_name='Test Owner',
                total_amount=1000.0,
                remaining_amount=500.0,
                max_players=15
            )
            db.session.add(team)
            
            # Create player
            player = Player(
                id=uuid.uuid4(),
                name='Test',
                last_name='Player',
                flat_no='101',
                age=25,
                mobile_number='1234567890',
                bowler_type='right',
                batter_type='right',
                category='avg',
                tournament_id=tournament.id
            )
            db.session.add(player)
            
            db.session.commit()
            
            self.test_user_id = str(test_user.id)
            self.tournament_id = str(tournament.id)
            self.team_id = str(team.id)
            self.player_id = str(player.id)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_export_tournament_details(self):
        """Test exporting tournament details as PDF"""
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
        
        # Test export endpoint
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get(f'/tournament/{self.tournament_id}/export-details', headers=headers)
        
        # Should return PDF file
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_export_tournament_summary(self):
        """Test exporting tournament summary as PDF"""
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
        
        # Test export endpoint
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get(f'/tournament/{self.tournament_id}/export-summary', headers=headers)
        
        # Should return PDF file
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_export_without_auth(self):
        """Test export without authentication"""
        response = self.client.get(f'/tournament/{self.tournament_id}/export-details')
        self.assertEqual(response.status_code, 401)

    def test_export_invalid_tournament(self):
        """Test export with invalid tournament ID"""
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
        response = self.client.get(f'/tournament/{invalid_id}/export-details', headers=headers)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main() 