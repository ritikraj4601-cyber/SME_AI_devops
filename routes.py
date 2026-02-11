from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Operation, DataLog
from utils import hash_password, verify_password, generate_token
from ai_engine import ai_engine

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'error': 'Missing fields'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    user = User(username=data['username'], email=data['email'], password=hash_password(data['password']))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not verify_password(data.get('password'), user.password):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = generate_token(user.id)
    return jsonify({'token': token}), 200

@api.route('/operations', methods=['GET'])
@jwt_required()
def get_operations():
    operations = Operation.query.all()
    return jsonify([{'id': o.id, 'name': o.name, 'status': o.status, 'predicted_outcome': o.predicted_outcome} for o in operations]), 200

@api.route('/operations', methods=['POST'])
@jwt_required()
def create_operation():
    data = request.get_json()
    operation = Operation(name=data['name'])
    db.session.add(operation)
    db.session.commit()
    return jsonify({'message': 'Operation created', 'id': operation.id}), 201

@api.route('/operations/<int:id>/automate', methods=['POST'])
@jwt_required()
def automate_operation(id):
    ai_engine.automate_operation(id)
    return jsonify({'message': 'Automation triggered'}), 200

@api.route('/insights', methods=['GET'])
@jwt_required()
def get_insights():
    logs = DataLog.query.all()
    insights = [{'operation_id': l.operation_id, 'metric': l.metric, 'value': l.value, 'timestamp': l.timestamp.isoformat()} for l in logs]
    return jsonify(insights), 200