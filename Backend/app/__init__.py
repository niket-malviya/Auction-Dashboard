from flask import Flask, request, jsonify
from .config import Config
from .extensions import db, jwt
from flask_cors import CORS
from services.jwt_service import handle_jwt_errors
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt, create_access_token
from datetime import datetime, timedelta
from models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return handle_jwt_errors(type('Error', (), {'code': 422})())

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return handle_jwt_errors(type('Error', (), {'code': 401})())

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return handle_jwt_errors(type('Error', (), {'code': 401})())

    # Global request interceptor for automatic token refresh
    @app.before_request
    def auto_refresh_token_middleware():
        # Skip for non-protected routes
        if request.endpoint in ['auth.login', 'auth.signup', 'auth.forgot_password_route', 'test_db.test_db']:
            return None
        
        # Skip for OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            return None
        
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None  # Let the route handle missing auth
        
        try:
            # Extract token
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return None  # Let the route handle invalid format
            
            token = parts[1]
            
            # Try to verify the token
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                token_data = get_jwt()
                
                # Check if token expires soon (within 5 minutes)
                exp_timestamp = token_data.get('exp')
                if exp_timestamp:
                    exp_datetime = datetime.fromtimestamp(exp_timestamp)
                    current_time = datetime.utcnow()
                    
                    if exp_datetime - current_time < timedelta(minutes=5):
                        # Token expires soon, create new one
                        user = User.query.get(current_user_id)
                        if user:
                            new_access_token = create_access_token(identity=str(user.id))
                            
                            # Store new token in app context for response modification
                            app.config['NEW_ACCESS_TOKEN'] = new_access_token
                            app.config['TOKEN_REFRESHED'] = True
                
            except Exception:
                # Token verification failed, let the route handle it
                pass
                
        except Exception:
            # Any other error, let the route handle it
            pass
        
        return None

    # Global response interceptor to add new tokens
    @app.after_request
    def add_new_token_to_response(response):
        if hasattr(app.config, 'NEW_ACCESS_TOKEN') and app.config.get('NEW_ACCESS_TOKEN'):
            # Add new token to response headers
            response.headers['X-New-Access-Token'] = app.config['NEW_ACCESS_TOKEN']
            response.headers['X-Token-Refreshed'] = 'true'
            
            # Also add to response body if it's JSON
            if response.content_type == 'application/json':
                try:
                    data = response.get_json()
                    if isinstance(data, dict):
                        data['new_access_token'] = app.config['NEW_ACCESS_TOKEN']
                        data['token_refreshed'] = True
                        response.set_data(jsonify(data).get_data())
                except Exception:
                    pass
            
            # Clear the stored token
            app.config.pop('NEW_ACCESS_TOKEN', None)
            app.config.pop('TOKEN_REFRESHED', None)
        
        return response

    # Import and register blueprints here
    from routes.test_db import test_db_bp
    app.register_blueprint(test_db_bp)
    from routes.auth_r import auth_bp
    app.register_blueprint(auth_bp)
    from routes.sport_type_r import sport_type_bp
    app.register_blueprint(sport_type_bp)
    from routes.player_r import player_bp
    app.register_blueprint(player_bp)
    from routes.team_r import team_bp
    app.register_blueprint(team_bp)
    from routes.tournament_r import tournament_bp
    app.register_blueprint(tournament_bp)
    from routes.unsold_players_r import unsold_player_bp
    app.register_blueprint(unsold_player_bp)
    from routes.team_player_r import team_player_bp
    app.register_blueprint(team_player_bp)
    from routes.export_r import export_bp
    app.register_blueprint(export_bp)
    from routes.import_r import import_bp
    app.register_blueprint(import_bp)

    return app
