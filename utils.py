from flask_jwt_extended import create_access_token
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def generate_token(user_id):
    return create_access_token(identity=user_id)