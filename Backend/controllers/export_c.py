# controllers/export_c.py
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from models.user import User
from services.pdf_export_service import TournamentPDFExportService
from models.tournament import Tournament

def admin_required(fn):
    """Decorator to ensure the user has admin privileges"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        if user.type not in ['admin', 'super_admin']:
            return jsonify({'message': 'Admin privileges required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Optional helper to export auction PDF (can be used in routes)
def export_auction_pdf_service(tournament_id):
    """Generate auction PDF using the service"""
    pdf_service = TournamentPDFExportService()
    buffer, error = pdf_service.export_auction_summary(tournament_id)
    return buffer, error
