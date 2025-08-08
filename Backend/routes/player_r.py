from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.player_c import (
    create_player, get_all_players, get_player_by_id,
    update_player, delete_player, get_players_by_tournament,
    import_players_from_excel
)
from models.user import User
import pandas as pd
from models.player import Player
from schemas.player_s import PlayerSchema
from app.extensions import db

player_bp = Blueprint('player', __name__)

def is_admin():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return user and user.type in ['admin', 'super_admin']

@player_bp.route('/players', methods=['POST'])
@jwt_required()
def create():
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can create players'}), 403
    data = request.json
    response = create_player(data)
    return jsonify(response), 201

@player_bp.route('/players', methods=['GET'])
@jwt_required()
def get_all():
    response = get_all_players()
    return jsonify(response), 200

@player_bp.route('/players/<uuid:player_id>', methods=['GET'])
@jwt_required()
def get_by_id(player_id):
    response = get_player_by_id(player_id)
    if response:
        return jsonify(response), 200
    return jsonify({'message': 'Player not found'}), 404

@player_bp.route('/players/<uuid:player_id>', methods=['PUT'])
@jwt_required()
def update(player_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can update players'}), 403
    data = request.json
    response = update_player(player_id, data)
    if response:
        return jsonify(response), 200
    return jsonify({'message': 'Player not found'}), 404

@player_bp.route('/players/<uuid:player_id>', methods=['DELETE'])
@jwt_required()
def delete(player_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can delete players'}), 403
    if delete_player(player_id):
        return jsonify({'message': 'Player deleted'}), 200
    return jsonify({'message': 'Player not found'}), 404

@player_bp.route('/tournaments/<uuid:tournament_id>/players', methods=['GET'])
@jwt_required()
def get_by_tournament(tournament_id):
    response = get_players_by_tournament(tournament_id)
    return jsonify(response), 200

@player_bp.route('/players/import', methods=['POST'])
@jwt_required()
def import_players():
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can import players'}), 403
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    result = import_players_from_excel(file)
    return jsonify(result), 201

@player_bp.route('/players/bulk', methods=['POST'])
@jwt_required()
def create_bulk():
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can create players'}), 403
    data = request.json  # Expecting a list of player dicts
    if not isinstance(data, list):
        return jsonify({'message': 'Input should be a list of player objects'}), 400
    created = []
    errors = []
    for idx, player_data in enumerate(data):
        try:
            response = create_player(player_data)
            created.append(response)
        except Exception as e:
            errors.append({'index': idx, 'error': str(e), 'data': player_data})
    return jsonify({'created': created, 'errors': errors}), 201
