from functools import wraps
from flask import request, jsonify, g
from flask_jwt_extended import (
    verify_jwt_in_request, 
    get_jwt_identity, 
    get_jwt,
    create_access_token,
    decode_token
)
from datetime import datetime, timedelta
from models.user import User
from app.extensions import db
import jwt

def auto_refresh_token():
    """Middleware to automatically refresh tokens before they expire"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # First, try to verify the current token
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                
                # Get token data
                token_data = get_jwt()
                exp_timestamp = token_data.get('exp')
                
                if exp_timestamp:
                    exp_datetime = datetime.fromtimestamp(exp_timestamp)
                    current_time = datetime.utcnow()
                    
                    # If token expires in less than 5 minutes, refresh it
                    if exp_datetime - current_time < timedelta(minutes=5):
                        # Create new access token
                        user = User.query.get(current_user_id)
                        if user:
                            new_access_token = create_access_token(identity=str(user.id))
                            
                            # Add new token to response headers
                            response = fn(*args, **kwargs)
                            if isinstance(response, tuple):
                                response_obj, status_code = response
                                if isinstance(response_obj, dict):
                                    response_obj['new_access_token'] = new_access_token
                                    response_obj['token_refreshed'] = True
                                    return jsonify(response_obj), status_code
                            else:
                                # If response is not a tuple, wrap it
                                response_data = response.get_json() if hasattr(response, 'get_json') else {}
                                response_data['new_access_token'] = new_access_token
                                response_data['token_refreshed'] = True
                                return jsonify(response_data)
                
                # Token is still valid, proceed normally
                return fn(*args, **kwargs)
                
            except Exception as e:
                # If token verification fails, return error
                return jsonify({
                    'message': 'Authentication required',
                    'error': 'AUTH_REQUIRED'
                }), 401
                
        return wrapper
    return decorator

def handle_expired_token():
    """Middleware to handle expired tokens gracefully"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                if 'expired' in str(e).lower():
                    return jsonify({
                        'message': 'Token has expired. Please refresh your session.',
                        'error': 'TOKEN_EXPIRED',
                        'requires_refresh': True
                    }), 422
                raise e
        return wrapper
    return decorator

def validate_user_session():
    """Middleware to validate user session and refresh if needed"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                return jsonify({
                    'message': 'Authorization header required',
                    'error': 'AUTH_HEADER_MISSING'
                }), 401
            
            try:
                # Extract token
                parts = auth_header.split()
                if len(parts) != 2 or parts[0].lower() != 'bearer':
                    return jsonify({
                        'message': 'Invalid authorization header format',
                        'error': 'INVALID_AUTH_FORMAT'
                    }), 401
                
                token = parts[1]
                
                # Decode token without verification to check expiry
                try:
                    decoded = jwt.decode(token, options={"verify_signature": False})
                except jwt.InvalidTokenError:
                    return jsonify({
                        'message': 'Invalid token format',
                        'error': 'INVALID_TOKEN_FORMAT'
                    }), 401
                
                # Check if token is expired
                exp_timestamp = decoded.get('exp')
                if exp_timestamp:
                    exp_datetime = datetime.fromtimestamp(exp_timestamp)
                    current_time = datetime.utcnow()
                    
                    if current_time > exp_datetime:
                        # Token is expired, try to get refresh token
                        refresh_token = request.headers.get('X-Refresh-Token')
                        
                        if refresh_token:
                            try:
                                # Verify refresh token
                                refresh_decoded = jwt.decode(
                                    refresh_token, 
                                    options={"verify_signature": False}
                                )
                                refresh_exp = refresh_decoded.get('exp')
                                
                                if refresh_exp and datetime.fromtimestamp(refresh_exp) > current_time:
                                    # Refresh token is valid, create new access token
                                    user_id = refresh_decoded.get('sub')
                                    user = User.query.get(user_id)
                                    
                                    if user:
                                        new_access_token = create_access_token(identity=str(user.id))
                                        
                                        # Execute the original function
                                        response = fn(*args, **kwargs)
                                        
                                        # Add new token to response
                                        if isinstance(response, tuple):
                                            response_obj, status_code = response
                                            if isinstance(response_obj, dict):
                                                response_obj['new_access_token'] = new_access_token
                                                response_obj['token_refreshed'] = True
                                                return jsonify(response_obj), status_code
                                        else:
                                            response_data = response.get_json() if hasattr(response, 'get_json') else {}
                                            response_data['new_access_token'] = new_access_token
                                            response_data['token_refreshed'] = True
                                            return jsonify(response_data)
                                
                            except Exception:
                                pass
                        
                        # If we get here, refresh failed or no refresh token
                        return jsonify({
                            'message': 'Token expired and refresh failed',
                            'error': 'TOKEN_EXPIRED_REFRESH_FAILED',
                            'requires_login': True
                        }), 422
                
                # Token is valid, proceed normally
                return fn(*args, **kwargs)
                
            except Exception as e:
                return jsonify({
                    'message': 'Authentication error',
                    'error': 'AUTH_ERROR'
                }), 401
                
        return wrapper
    return decorator

def admin_required_with_auto_refresh():
    """Admin check with automatic token refresh"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                user = User.query.get(current_user_id)
                
                if not user:
                    return jsonify({
                        'message': 'User not found',
                        'error': 'USER_NOT_FOUND'
                    }), 404
                
                if user.type not in ['admin', 'super_admin']:
                    return jsonify({
                        'message': 'Admin privileges required',
                        'error': 'ADMIN_REQUIRED'
                    }), 403
                
                # Check token expiry and refresh if needed
                token_data = get_jwt()
                exp_timestamp = token_data.get('exp')
                
                if exp_timestamp:
                    exp_datetime = datetime.fromtimestamp(exp_timestamp)
                    current_time = datetime.utcnow()
                    
                    if exp_datetime - current_time < timedelta(minutes=5):
                        new_access_token = create_access_token(identity=str(user.id))
                        
                        response = fn(*args, **kwargs)
                        if isinstance(response, tuple):
                            response_obj, status_code = response
                            if isinstance(response_obj, dict):
                                response_obj['new_access_token'] = new_access_token
                                response_obj['token_refreshed'] = True
                                return jsonify(response_obj), status_code
                        else:
                            response_data = response.get_json() if hasattr(response, 'get_json') else {}
                            response_data['new_access_token'] = new_access_token
                            response_data['token_refreshed'] = True
                            return jsonify(response_data)
                
                return fn(*args, **kwargs)
                
            except Exception as e:
                return jsonify({
                    'message': 'Authentication required',
                    'error': 'AUTH_REQUIRED'
                }), 401
                
        return wrapper
    return decorator 