import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'agri-smart-secret-2024')

    # Fix: Render gives postgres:// but SQLAlchemy needs postgresql://
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///agri.db')
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # ML Model paths
    SOIL_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'soil_model.pkl')
    DISEASE_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'disease_model.h5')
    PRICE_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'price_model.pkl')
