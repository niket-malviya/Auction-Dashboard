from flask import Blueprint, send_file, jsonify
from flask_jwt_extended import jwt_required
from controllers.export_c import admin_required, export_auction_pdf_service
from models.tournament import Tournament

export_bp = Blueprint('export', __name__)

@export_bp.route('/tournament/<tournament_id>/export-auction', methods=['GET'])
@jwt_required()
@admin_required
def export_auction_pdf(tournament_id):
    """Export completed auction details as PDF"""
    buffer, error = export_auction_pdf_service(tournament_id)
    
    if error:
        return jsonify({'message': error}), 400

    tournament = Tournament.query.get(tournament_id)
    if not tournament:
        return jsonify({'message': 'Tournament not found'}), 404

    filename = f"auction_{tournament.name.replace(' ', '_')}.pdf"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )
