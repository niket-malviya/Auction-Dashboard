from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.sport_type_c import create_sport_type, get_all_sport_types, get_sport_type_by_id, update_sport_type, delete_sport_type
from models.user import User

sport_type_bp = Blueprint('sport_type', __name__)

def is_admin():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return user and user.type in ['admin', 'super_admin']

@sport_type_bp.route('/sport-types', methods=['POST'])
@jwt_required()
def create():
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can create sport types'}), 403
    data = request.json
    response = create_sport_type(data)
    return jsonify(response), 201

@sport_type_bp.route('/sport-types', methods=['GET'])
@jwt_required()
def get_all():
    response = get_all_sport_types()
    return jsonify(response), 200

@sport_type_bp.route('/sport-types/<uuid:sport_id>', methods=['GET'])
@jwt_required()
def get_by_id(sport_id):
    response = get_sport_type_by_id(sport_id)
    if response:
        return jsonify(response), 200
    return jsonify({'message': 'Sport type not found'}), 404

@sport_type_bp.route('/sport-types/<uuid:sport_id>', methods=['PUT'])
@jwt_required()
def update(sport_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can update sport types'}), 403
    data = request.json
    response = update_sport_type(sport_id, data)
    if response:
        return jsonify(response), 200
    return jsonify({'message': 'Sport type not found'}), 404

@sport_type_bp.route('/sport-types/<uuid:sport_id>', methods=['DELETE'])
@jwt_required()
def delete(sport_id):
    if not is_admin():
        return jsonify({'message': 'Unauthorized. Only admins can delete sport types'}), 403
    if delete_sport_type(sport_id):
        return jsonify({'message': 'Sport type deleted'}), 200
    return jsonify({'message': 'Sport type not found'}), 404

