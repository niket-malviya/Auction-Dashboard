from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from datetime import datetime, timedelta
from models.user import User
from app.extensions import db

class JWTService:
    @staticmethod
    def create_tokens(user_id):
        """Create both access and refresh tokens for a user"""
        access_token = create_access_token(identity=str(user_id))
        refresh_token = create_refresh_token(identity=str(user_id))
        return access_token, refresh_token
    
    @staticmethod
    def refresh_access_token():
        """Refresh access token using refresh token"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return None, "User not found"
        
        new_access_token = create_access_token(identity=str(user.id))
        return new_access_token, user
    
    @staticmethod
    def get_current_user():
        """Get current user from JWT token"""
        current_user_id = get_jwt_identity()
        return User.query.get(current_user_id)
    
    @staticmethod
    def is_token_expired(token_data):
        """Check if token is expired"""
        if not token_data:
            return True
        
        exp_timestamp = token_data.get('exp')
        if not exp_timestamp:
            return True
        
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        return datetime.utcnow() > exp_datetime
    
    @staticmethod
    def get_token_expiry(token_data):
        """Get token expiry datetime"""
        if not token_data:
            return None
        
        exp_timestamp = token_data.get('exp')
        if not exp_timestamp:
            return None
        
        return datetime.fromtimestamp(exp_timestamp)
    
    @staticmethod
    def validate_user_permissions(user, required_type=None):
        """Validate user permissions"""
        if not user:
            return False, "User not found"
        
        if required_type and user.type not in required_type:
            return False, "Insufficient permissions"
        
        return True, "Valid user"

# Error handlers for JWT
def handle_jwt_errors(error):
    """Handle JWT errors and return appropriate responses"""
    if error.code == 401:
        return {
            'message': 'Token is missing or invalid',
            'error': 'UNAUTHORIZED'
        }, 401
    elif error.code == 422:
        return {
            'message': 'Token is expired',
            'error': 'TOKEN_EXPIRED'
        }, 422
    else:
        return {
            'message': 'Token validation failed',
            'error': 'TOKEN_INVALID'
        }, 400 