from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.team_player_c import (
    create_team_player, get_all_team_players, get_team_player_by_keys, get_all_team_players_by_team_id, delete_team_player
)
from models.team_player import TeamPlayer
from models.user import User

team_player_bp = Blueprint('team_player', __name__)

def is_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.type in ['admin', 'super_admin']

@team_player_bp.route('/team_players', methods=['POST'])
@jwt_required()
def add_team_player():
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can add team players'}), 403
    data = request.json
    player_id = data.get('player_id')
    tournament_id = data.get('tournament_id')
    existing = TeamPlayer.query.filter_by(player_id=player_id, tournament_id=tournament_id).first()
    if existing:
        return jsonify({'message': 'Player already assigned to a team in this tournament.'}), 400
    response = create_team_player(data)
    return jsonify(response), 201
# @team_player_bp.route('/team_players', methods=['POST'])
# def add_team_player():
#     # ⚠️ TEMPORARY WARNING: This bypasses admin check!
#     # Remove this in production or when auth is ready.

#     data = request.json
#     player_id = data.get('player_id')
#     tournament_id = data.get('tournament_id')

#     existing = TeamPlayer.query.filter_by(player_id=player_id, tournament_id=tournament_id).first()
#     if existing:
#         return jsonify({'message': 'Player already assigned to a team in this tournament.'}), 400

#     response = create_team_player(data)
#     return jsonify(response), 201

@team_player_bp.route('/team_players', methods=['GET'])
@jwt_required()
def list_team_players():
    response = get_all_team_players()
    return jsonify(response), 200

@team_player_bp.route('/team_players/<uuid:team_id>/<uuid:player_id>/<uuid:tournament_id>', methods=['DELETE'])
@jwt_required()
def remove_team_player(team_id, player_id, tournament_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can remove team players'}), 403
    result = delete_team_player(team_id, player_id, tournament_id)
    if result:
        return jsonify({'message': 'Player removed from team.'}), 200
    return jsonify({'message': 'Team player record not found.'}), 404

@team_player_bp.route('/team_players/<uuid:team_id>/<uuid:player_id>/<uuid:tournament_id>', methods=['GET'])
@jwt_required(optional=True)
def get_team_player(team_id, player_id, tournament_id):
    from controllers.team_player_c import get_team_player_by_keys
    result = get_team_player_by_keys(team_id, player_id, tournament_id)
    if result:
        return jsonify(result), 200
    return jsonify({'message': 'Team player record not found.'}), 404

@team_player_bp.route('/team_players/team/<uuid:team_id>', methods=['GET'])
@jwt_required(optional=True)
def get_team_players_by_team(team_id):
    from controllers.team_player_c import get_all_team_players_by_team_id
    result = get_all_team_players_by_team_id(team_id)
    return jsonify(result), 200 