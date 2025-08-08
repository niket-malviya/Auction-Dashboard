from flask import Blueprint, jsonify
from app.extensions import db

test_db_bp = Blueprint('test_db', __name__)

@test_db_bp.route('/test-db')
def test_db():
    try:
        db.session.execute('SELECT 1')
        return jsonify({'status': 'success', 'message': 'Database connected!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
