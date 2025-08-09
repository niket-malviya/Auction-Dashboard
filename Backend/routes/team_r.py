from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.team_c import (
    create_team, get_team_by_id, get_all_teams, update_team, delete_team, get_teams_by_tournament
)
from models.user import User

team_bp = Blueprint('team', __name__)

def is_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.type in ['admin', 'super_admin']

@team_bp.route('/teams', methods=['POST'])
@jwt_required()
def create_team_route():
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can create teams'}), 403
    data = request.json
    result = create_team(data)
    return jsonify(result), 201

@team_bp.route('/teams/<uuid:team_id>', methods=['PUT'])
@jwt_required()
def update_team_route(team_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can update teams'}), 403
    data = request.json
    result = update_team(team_id, data)
    if result:
        return jsonify(result), 200
    return jsonify({'message': 'Team not found'}), 404

@team_bp.route('/teams/<uuid:team_id>', methods=['DELETE'])
@jwt_required()
def delete_team_route(team_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can delete teams'}), 403
    result = delete_team(team_id)
    if result:
        return jsonify({'message': 'Team deleted'}), 200
    return jsonify({'message': 'Team not found'}), 404

@team_bp.route('/teams', methods=['GET'])
def get_teams():
    result = get_all_teams()
    return jsonify(result), 200

@team_bp.route('/teams/<uuid:team_id>', methods=['GET'])
def get_team_by_id_route(team_id):
    result = get_team_by_id(team_id)
    if result:
        return jsonify(result), 200
    return jsonify({'message': 'Team not found'}), 404

@team_bp.route('/tournaments/<uuid:tournament_id>/teams', methods=['GET'])
def get_teams_by_tournament_route(tournament_id):
    result = get_teams_by_tournament(tournament_id)
    return jsonify(result), 200
