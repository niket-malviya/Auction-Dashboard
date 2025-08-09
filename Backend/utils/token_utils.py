import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps

def decode_token(token):
    """Decode JWT token without verification (for frontend use)"""
    try:
        return jwt.decode(token, options={"verify_signature": False})
    except jwt.InvalidTokenError:
        return None

def is_token_expired(token):
    """Check if token is expired (for frontend use)"""
    decoded = decode_token(token)
    if not decoded:
        return True
    
    exp_timestamp = decoded.get('exp')
    if not exp_timestamp:
        return True
    
    exp_datetime = datetime.fromtimestamp(exp_timestamp)
    return datetime.utcnow() > exp_datetime

def should_refresh_token(token, buffer_minutes=5):
    """Check if token should be refreshed (for frontend use)"""
    decoded = decode_token(token)
    if not decoded:
        return True
    
    exp_timestamp = decoded.get('exp')
    if not exp_timestamp:
        return True
    
    exp_datetime = datetime.fromtimestamp(exp_timestamp)
    buffer_time = datetime.utcnow() + timedelta(minutes=buffer_minutes)
    return buffer_time > exp_datetime

def get_token_from_header():
    """Extract token from Authorization header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    
    return parts[1]

def token_required(f):
    """Decorator to require valid token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        if is_token_expired(token):
            return jsonify({'message': 'Token is expired', 'error': 'TOKEN_EXPIRED'}), 422
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        decoded = decode_token(token)
        if not decoded:
            return jsonify({'message': 'Invalid token'}), 401
        
        # You might want to check user type from database here
        # For now, we'll assume the token contains user info
        user_type = decoded.get('user_type', 'user')
        if user_type not in ['admin', 'super_admin']:
            return jsonify({'message': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function 