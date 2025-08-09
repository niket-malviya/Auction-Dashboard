from models.team_player import TeamPlayer
from models.player import Player
from schemas.team_player_s import TeamPlayerSchema
from app.extensions import db
from models.team import Team
import pdb

team_player_schema = TeamPlayerSchema()
team_players_schema = TeamPlayerSchema(many=True)

# def create_team_player(data):
#     validated_data = team_player_schema.load(data)
#     player_id = validated_data.get('player_id')
#     tournament_id = validated_data.get('tournament_id')
#     team_id = validated_data.get('team_id')
#     existing = TeamPlayer.query.filter_by(player_id=player_id, tournament_id=tournament_id).first()
#     if existing:
#         return None
#     new_team_player = TeamPlayer(**validated_data)
#     db.session.add(new_team_player)
    
#     # Update player status to 'sold'
#     player = Player.query.get(player_id)
#     if player:
#         player.status = 'sold'
    
#     db.session.commit()
#     return team_player_schema.dump(new_team_player)

def create_team_player(data):
    #pdb.set_trace();
    validated_data = team_player_schema.load(data)
    player_id = validated_data.get('player_id')
    tournament_id = validated_data.get('tournament_id')
    team_id = validated_data.get('team_id')
    bid_amount = validated_data.get('bid_amount')  # Ensure this is passed from frontend

    # Prevent assigning player more than once
    existing = TeamPlayer.query.filter_by(player_id=player_id, tournament_id=tournament_id).first()
    if existing:
        return None

    # Fetch team and player from DB
    team = Team.query.get(team_id)
    player = Player.query.get(player_id)

    if not team or not player:
        return None

    # pdb.set_trace()

    # Create team-player link
    new_team_player = TeamPlayer(**validated_data)
    db.session.add(new_team_player)

    # Update player status
    player.status = 'sold'

    # Update team budget and player counts
    team.remaining_amount = int(team.remaining_amount) - bid_amount
    team.total_players = int(team.total_players) + 1

    # Update category count
    if player.category == 'gold':
        team.gold = int(team.gold) + 1
    elif player.category == 'silver':
        team.silver = int(team.silver) + 1
    elif player.category == 'bronze':
        team.bronze = int(team.bronze) + 1

    db.session.commit()

    return team_player_schema.dump(new_team_player)



def delete_team_player(team_id, player_id, tournament_id):
    team_player = TeamPlayer.query.filter_by(team_id=team_id, player_id=player_id, tournament_id=tournament_id).first()
    if not team_player:
        return None
    db.session.delete(team_player)
    
    # Update player status back to 'unsold'
    player = Player.query.get(player_id)
    if player:
        player.status = 'unsold'
    
    db.session.commit()
    return True

def get_team_player_by_keys(team_id, player_id, tournament_id):
    team_player = TeamPlayer.query.filter_by(team_id=team_id, player_id=player_id, tournament_id=tournament_id).first()
    if team_player:
        return team_player_schema.dump(team_player)
    return None

def get_all_team_players_by_team_id(team_id):
    team_players = TeamPlayer.query.filter_by(team_id=team_id).all()
    return team_players_schema.dump(team_players)

def get_all_team_players():
    team_players = TeamPlayer.query.all()
    return team_players_schema.dump(team_players)
