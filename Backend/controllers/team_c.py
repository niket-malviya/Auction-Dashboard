from models.team import Team
from schemas.team_s import TeamSchema
from app.extensions import db

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

def create_team(data):
    validated_data = team_schema.load(data)
    new_team = Team(**validated_data)
    db.session.add(new_team)
    db.session.commit()
    return team_schema.dump(new_team)

def get_team_by_id(team_id):
    team = Team.query.get(team_id)
    if team:
        return team_schema.dump(team)
    return None

def get_all_teams():
    teams = Team.query.all()
    return teams_schema.dump(teams)

def update_team(team_id, data):
    team = Team.query.get(team_id)
    if team:
        validated_data = team_schema.load(data, partial=True)
        for key, value in validated_data.items():
            setattr(team, key, value)
        db.session.commit()
        return team_schema.dump(team)
    return None

def delete_team(team_id):
    team = Team.query.get(team_id)
    if team:
        db.session.delete(team)
        db.session.commit()
        return True
    return False

def get_team_players(team_id):
    team = Team.query.get(team_id)
    if team:
        return [team_player.player for team_player in team.team_players]
    return None

def get_teams_by_tournament(tournament_id):
    from models.team_player import TeamPlayer
    teams = (
        Team.query
        .join(TeamPlayer, Team.id == TeamPlayer.team_id)
        .filter(TeamPlayer.tournament_id == tournament_id)
        .all()
    )
    return teams_schema.dump(teams)
