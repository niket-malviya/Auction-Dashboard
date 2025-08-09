import pandas as pd
from models.player import Player
from schemas.player_s import PlayerSchema
from app.extensions import db

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)

def create_player(data):
    validated_data = player_schema.load(data)
    new_player = Player(**validated_data)
    db.session.add(new_player)
    db.session.commit()
    return player_schema.dump(new_player)

def get_all_players():
    players = Player.query.all()
    return players_schema.dump(players)

def get_player_by_id(player_id):
    player = Player.query.get(player_id)
    if player:
        return player_schema.dump(player)
    return None

def update_player(player_id, data):
    player = Player.query.get(player_id)
    if player:
        validated_data = player_schema.load(data, partial=True)
        for key, value in validated_data.items():
            setattr(player, key, value)
        db.session.commit()
        return player_schema.dump(player)
    return None

def delete_player(player_id):
    player = Player.query.get(player_id)
    if player:
        db.session.delete(player)
        db.session.commit()
        return True
    return False

def get_players_by_tournament(tournament_id):
    players = Player.query.filter_by(tournament_id=tournament_id).all()
    return players_schema.dump(players)

def import_players_from_excel(file):
    df = pd.read_excel(file)
    player_schema = PlayerSchema()
    imported = []
    errors = []
    for _, row in df.iterrows():
        try:
            data = row.to_dict()
            # Validate and load data
            player_data = player_schema.load(data)
            new_player = Player(**player_data)
            db.session.add(new_player)
            imported.append(player_data)
        except Exception as e:
            errors.append({'row': row.to_dict(), 'error': str(e)})
    db.session.commit()
    return {'imported': imported, 'errors': errors}
