from database.db import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    lands = db.relationship('LandRecord', backref='owner', lazy=True)
    soil_analyses = db.relationship('SoilAnalysis', backref='owner', lazy=True)
    diseases = db.relationship('CropDisease', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'


class LandRecord(db.Model):
    __tablename__ = 'land_records'
    land_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    area = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    soil_type = db.Column(db.String(100))
    crop_grown = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'land_id': self.land_id,
            'area': self.area,
            'location': self.location,
            'soil_type': self.soil_type,
            'crop_grown': self.crop_grown,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class SoilAnalysis(db.Model):
    __tablename__ = 'soil_analysis'
    analysis_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    ph = db.Column(db.Float)
    moisture = db.Column(db.Float)
    nitrogen = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    result = db.Column(db.String(200))
    recommended_crops = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'analysis_id': self.analysis_id,
            'ph': self.ph,
            'moisture': self.moisture,
            'nitrogen': self.nitrogen,
            'phosphorus': self.phosphorus,
            'potassium': self.potassium,
            'result': self.result,
            'recommended_crops': self.recommended_crops,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class CropDisease(db.Model):
    __tablename__ = 'crop_diseases'
    disease_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    image_path = db.Column(db.String(300))
    crop_name = db.Column(db.String(100))
    prediction = db.Column(db.String(200))
    solution = db.Column(db.Text)
    confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'disease_id': self.disease_id,
            'crop_name': self.crop_name,
            'prediction': self.prediction,
            'solution': self.solution,
            'confidence': self.confidence,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class PricePrediction(db.Model):
    __tablename__ = 'price_predictions'
    prediction_id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    market = db.Column(db.String(100))
    predicted_price = db.Column(db.Float)
    unit = db.Column(db.String(20), default='quintal')
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'prediction_id': self.prediction_id,
            'crop_name': self.crop_name,
            'state': self.state,
            'market': self.market,
            'predicted_price': self.predicted_price,
            'unit': self.unit,
            'date': self.date.strftime('%Y-%m-%d')
        }
    
    # ADD at the bottom of database/models.py — after PricePrediction class

class LandRegistry(db.Model):
    """Public land registry — 1000 seeded records, searchable by all users"""
    __tablename__ = 'land_registry'
    id            = db.Column(db.Integer, primary_key=True)
    khata_no      = db.Column(db.String(20), index=True)
    khesra_no     = db.Column(db.String(20), index=True)
    survey_no     = db.Column(db.String(20))
    owner_name    = db.Column(db.String(100), index=True)
    state         = db.Column(db.String(100), index=True)
    city          = db.Column(db.String(100), index=True)
    area          = db.Column(db.Float)
    soil_type     = db.Column(db.String(100))
    land_type     = db.Column(db.String(50))
    crop_history  = db.Column(db.String(200))
    water_source  = db.Column(db.String(100))
    land_status   = db.Column(db.String(50))
    registered_year = db.Column(db.Integer)
    ph_value      = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'khata_no': self.khata_no,
            'khesra_no': self.khesra_no,
            'survey_no': self.survey_no,
            'owner_name': self.owner_name,
            'state': self.state,
            'city': self.city,
            'area': self.area,
            'soil_type': self.soil_type,
            'land_type': self.land_type,
            'crop_history': self.crop_history,
            'water_source': self.water_source,
            'land_status': self.land_status,
            'registered_year': self.registered_year,
            'ph_value': self.ph_value,
        }


class LandAnalysis(db.Model):
    """Stores AI land image analysis results per user"""
    __tablename__ = 'land_analysis'
    analysis_id   = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    image_path    = db.Column(db.String(300))
    ph            = db.Column(db.Float)
    nitrogen      = db.Column(db.Float)
    phosphorus    = db.Column(db.Float)
    potassium     = db.Column(db.Float)
    organic_matter = db.Column(db.Float)
    moisture      = db.Column(db.Float)
    health_score  = db.Column(db.Float)
    quality       = db.Column(db.String(50))
    texture       = db.Column(db.String(50))
    suitable_crops = db.Column(db.Text)
    fertilizer    = db.Column(db.Text)
    irrigation    = db.Column(db.Text)
    summary       = db.Column(db.Text)
    created_at    = db.Column(db.DateTime, default=__import__('datetime').datetime.utcnow)

    def to_dict(self):
        return {
            'analysis_id': self.analysis_id,
            'ph': self.ph,
            'nitrogen': self.nitrogen,
            'phosphorus': self.phosphorus,
            'potassium': self.potassium,
            'organic_matter': self.organic_matter,
            'moisture': self.moisture,
            'health_score': self.health_score,
            'quality': self.quality,
            'texture': self.texture,
            'suitable_crops': self.suitable_crops,
            'fertilizer': self.fertilizer,
            'irrigation': self.irrigation,
            'summary': self.summary,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
        }
