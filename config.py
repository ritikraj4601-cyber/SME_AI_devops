import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-key-change-this'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://...'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'fallback-jwt-key-change-this'
    SCHEDULER_API_ENABLED = True