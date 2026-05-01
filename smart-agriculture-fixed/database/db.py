from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize database with the app"""
    db.init_app(app)
    with app.app_context():
        from database.models import User, LandRecord, SoilAnalysis, CropDisease, PricePrediction
        db.create_all()
