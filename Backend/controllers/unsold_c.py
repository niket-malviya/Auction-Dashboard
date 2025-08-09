from models.unsold_player import UnsoldPlayer
from models.player import Player
from schemas.unsold_s import UnsoldPlayerSchema
from app.extensions import db
from models.team_player import TeamPlayer

unsold_player_schema = UnsoldPlayerSchema()
unsold_players_schema = UnsoldPlayerSchema(many=True)

def create_unsold_player(data):
    validated_data = unsold_player_schema.load(data)
    player_id = validated_data.get('player_id')
    tournament_id = validated_data.get('tournament_id')
    # Only add as unsold if not assigned to any team in this tournament
    assigned = TeamPlayer.query.filter_by(player_id=player_id, tournament_id=tournament_id).first()
    if assigned:
        return None  # Or return a specific error dict if you want
    new_unsold = UnsoldPlayer(**validated_data)
    db.session.add(new_unsold)
    
    # Update player status to 'unsold'
    player = Player.query.get(player_id)
    if player:
        player.status = 'unsold'
    
    db.session.commit()
    return unsold_player_schema.dump(new_unsold)

def get_all_unsold_players():
    unsold_players = UnsoldPlayer.query.all()
    return unsold_players_schema.dump(unsold_players)

def get_unsold_player_by_id(unsold_id):
    unsold = UnsoldPlayer.query.get(unsold_id)
    if unsold:
        return unsold_player_schema.dump(unsold)
    return None

def delete_unsold_player(unsold_id):
    unsold = UnsoldPlayer.query.get(unsold_id)
    if not unsold:
        return None
    db.session.delete(unsold)
    db.session.commit()
    return True
