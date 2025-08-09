import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from models.user import User
from app.extensions import db

def signup_user(data):
    if User.query.filter_by(email=data['email']).first():
        return {'message': 'User already exists'}, 400
    hashed_pw = generate_password_hash(data['password'])
    new_user = User(
        id=uuid.uuid4(),
        name=data['name'],
        email=data['email'],
        password=hashed_pw,
        type=data['type']
    )
    db.session.add(new_user)
    db.session.commit()
    return {'message': 'User created'}, 201

def login_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
                'type': user.type
            }
        }, 200
    return {'message': 'Invalid credentials'}, 401

def refresh_token():
    """Refresh access token using refresh token"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return {'message': 'User not found'}, 404
    
    new_access_token = create_access_token(identity=str(user.id))
    return {
        'access_token': new_access_token,
        'user': {
            'id': str(user.id),
            'name': user.name,
            'email': user.email,
            'type': user.type
        }
    }, 200

def forgot_password(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return {'message': 'Email not found'}, 404
    new_password = data.get('new_password')
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return {'message': 'Password updated'}, 200
