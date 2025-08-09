from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.export_c import export_tournament_pdf, get_export_options
from models.user import User

export_bp = Blueprint('export', __name__)

@export_bp.route('/tournament/<tournament_id>/export', methods=['GET'])
@jwt_required()
def export_tournament(tournament_id):
    """Export tournament details as PDF"""
    # Get current user
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Check if user has admin privileges
    if user.type not in ['admin', 'super_admin']:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    # Get export type from query parameters
    export_type = request.args.get('type', 'details')
    
    if export_type not in ['details', 'summary']:
        return jsonify({'message': 'Invalid export type. Use "details" or "summary"'}), 400
    
    return export_tournament_pdf(tournament_id, export_type)

@export_bp.route('/tournament/<tournament_id>/export-options', methods=['GET'])
@jwt_required()
def get_tournament_export_options(tournament_id):
    """Get available export options for a tournament"""
    # Get current user
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Check if user has admin privileges
    if user.type not in ['admin', 'super_admin']:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    response, status = get_export_options(tournament_id)
    return jsonify(response), status

@export_bp.route('/tournament/<tournament_id>/export-details', methods=['GET'])
@jwt_required()
def export_tournament_details(tournament_id):
    """Export full tournament details as PDF"""
    # Get current user
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Check if user has admin privileges
    if user.type not in ['admin', 'super_admin']:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    return export_tournament_pdf(tournament_id, 'details')

@export_bp.route('/tournament/<tournament_id>/export-summary', methods=['GET'])
@jwt_required()
def export_tournament_summary(tournament_id):
    """Export tournament summary as PDF"""
    # Get current user
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Check if user has admin privileges
    if user.type not in ['admin', 'super_admin']:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    return export_tournament_pdf(tournament_id, 'summary') 