from models.tournament import Tournament
from schemas.tournament_s import TournamentSchema
from app import db

tournament_schema = TournamentSchema()
tournaments_schema = TournamentSchema(many=True)

def create_tournament(data):
    if 'user_id' in data:
        data['users_id'] = data.pop('user_id')
    validated_data = tournament_schema.load(data)
    new_tournament = Tournament(**validated_data)
    db.session.add(new_tournament)
    db.session.commit()
    return tournament_schema.dump(new_tournament)

def get_all_tournaments():
    tournaments = Tournament.query.all()
    return tournaments_schema.dump(tournaments)

def get_tournament_by_id(tournament_id):
    tournament = Tournament.query.get(tournament_id)
    if tournament:
        return tournament_schema.dump(tournament)
    return None

def update_tournament(tournament_id, data):
    tournament = Tournament.query.get(tournament_id)
    if tournament:
        if 'user_id' in data:
            data['users_id'] = data.pop('user_id')
        validated_data = tournament_schema.load(data, partial=True)
        for key, value in validated_data.items():
            setattr(tournament, key, value)
        db.session.commit()
        return tournament_schema.dump(tournament)
    return None

def delete_tournament(tournament_id):
    tournament = Tournament.query.get(tournament_id)
    if tournament:
        db.session.delete(tournament)
        db.session.commit()
        return True
    return False
