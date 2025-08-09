from flask import request, jsonify, send_file
from services.excel_import_service import ExcelImportService
from models.tournament import Tournament
from models.user import User
from flask_jwt_extended import get_jwt_identity
import logging

def import_players_from_excel(tournament_id):
    """Import players from Excel file"""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Check if user has admin privileges
        if user.type not in ['admin', 'super_admin']:
            return jsonify({'message': 'Admin privileges required'}), 403
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'message': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file is empty
        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400
        
        # Create Excel import service
        import_service = ExcelImportService()
        
        # Import players
        success, message, details = import_service.import_players_from_excel(file, tournament_id)
        
        if success:
            return jsonify({
                'message': message,
                'details': details
            }), 200
        else:
            return jsonify({
                'message': message,
                'details': details
            }), 400
            
    except Exception as e:
        logging.error(f"Import controller error: {str(e)}")
        return jsonify({'message': f'Import failed: {str(e)}'}), 500

def get_excel_template():
    """Get Excel template for player import"""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Check if user has admin privileges
        if user.type not in ['admin', 'super_admin']:
            return jsonify({'message': 'Admin privileges required'}), 403
        
        # Create Excel import service
        import_service = ExcelImportService()
        
        # Generate template
        template_buffer = import_service.get_excel_template()
        
        if template_buffer:
            return send_file(
                template_buffer,
                as_attachment=True,
                download_name='player_import_template.xlsx',
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            return jsonify({'message': 'Error generating template'}), 500
            
    except Exception as e:
        logging.error(f"Template generation error: {str(e)}")
        return jsonify({'message': f'Template generation failed: {str(e)}'}), 500

def validate_excel_file(tournament_id):
    """Validate Excel file before import"""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Check if user has admin privileges
        if user.type not in ['admin', 'super_admin']:
            return jsonify({'message': 'Admin privileges required'}), 403
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'message': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file is empty
        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400
        
        # Create Excel import service
        import_service = ExcelImportService()
        
        # Validate file
        is_valid, message = import_service.validate_excel_file(file)
        
        if is_valid:
            return jsonify({
                'message': 'File is valid',
                'valid': True
            }), 200
        else:
            return jsonify({
                'message': message,
                'valid': False
            }), 400
            
    except Exception as e:
        logging.error(f"File validation error: {str(e)}")
        return jsonify({'message': f'Validation failed: {str(e)}'}), 500 