from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from controllers.unsold_c import (
    create_unsold_player, get_all_unsold_players
)

unsold_player_bp = Blueprint('unsold_player', __name__)

@unsold_player_bp.route('/unsold_players', methods=['POST'])
@jwt_required()
def add_unsold_player():
    data = request.json
    response = create_unsold_player(data)
    return jsonify(response), 201

@unsold_player_bp.route('/unsold_players', methods=['GET'])
@jwt_required()
def list_unsold_players():
    response = get_all_unsold_players()
    return jsonify(response), 200
