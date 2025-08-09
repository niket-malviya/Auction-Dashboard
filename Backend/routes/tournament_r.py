from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.tournament_c import (
    create_tournament, get_all_tournaments, get_tournament_by_id,
    update_tournament, delete_tournament
)
from models.user import User

tournament_bp = Blueprint('tournament', __name__)

def is_admin():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return user and user.type in ['admin', 'super_admin']

@tournament_bp.route('/tournament', methods=['POST'])
@jwt_required()
def create():
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can create tournaments'}), 403
    data = request.json
    response = create_tournament(data)
    return jsonify(response), 201

@tournament_bp.route('/get_all_tournament', methods=['GET'])
@jwt_required()
def get_all():
    response = get_all_tournaments()
    return jsonify(response), 200

@tournament_bp.route('/by_id_tournament/<uuid:tournament_id>', methods=['GET'])
@jwt_required()
def get_by_id(tournament_id):
    response = get_tournament_by_id(tournament_id)
    if response:
        return jsonify(response), 200
    return jsonify({'message': 'Tournament not found'}), 404

@tournament_bp.route('/update_tournament/<uuid:tournament_id>', methods=['PUT'])
@jwt_required()
def update(tournament_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can update tournaments'}), 403
    data = request.json
    response = update_tournament(tournament_id, data)
    if response:
        return jsonify(response), 200
    return jsonify({'message': 'Tournament not found'}), 404

@tournament_bp.route('/delete_tournament/<uuid:tournament_id>', methods=['DELETE'])
@jwt_required()
def delete(tournament_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can delete tournaments'}), 403
    if delete_tournament(tournament_id):
        return jsonify({'message': 'Tournament deleted'}), 200
    return jsonify({'message': 'Tournament not found'}), 404
