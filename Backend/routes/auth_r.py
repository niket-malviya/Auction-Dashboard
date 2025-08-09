from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from controllers.auth_c import signup_user, login_user, forgot_password, refresh_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    response, status = signup_user(data)
    return jsonify(response), status

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    response, status = login_user(data)
    return jsonify(response), status

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    response, status = refresh_token()
    return jsonify(response), status

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password_route():
    data = request.json
    response, status = forgot_password(data)
    return jsonify(response), status
