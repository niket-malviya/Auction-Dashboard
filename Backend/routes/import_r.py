from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from controllers.import_c import import_players_from_excel, get_excel_template, validate_excel_file

import_bp = Blueprint('import', __name__)

@import_bp.route('/tournament/<tournament_id>/import-players', methods=['POST'])
@jwt_required()
def import_players(tournament_id):
    """Import players from Excel file"""
    return import_players_from_excel(tournament_id)

@import_bp.route('/tournament/<tournament_id>/validate-excel', methods=['POST'])
@jwt_required()
def validate_excel(tournament_id):
    """Validate Excel file before import"""
    return validate_excel_file(tournament_id)

@import_bp.route('/excel-template', methods=['GET'])
@jwt_required()
def download_template():
    """Download Excel template for player import"""
    return get_excel_template()

@import_bp.route('/tournament/<tournament_id>/import-status', methods=['GET'])
@jwt_required()
def get_import_status(tournament_id):
    """Get import status and statistics"""
    try:
        from models.player import Player
        from models.tournament import Tournament
        
        # Check if tournament exists
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            return jsonify({'message': 'Tournament not found'}), 404
        
        # Get player statistics
        total_players = Player.query.filter_by(tournament_id=tournament_id).count()
        
        return jsonify({
            'tournament_id': tournament_id,
            'tournament_name': tournament.name,
            'total_players': total_players,
            'import_ready': True
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error getting import status: {str(e)}'}), 500 