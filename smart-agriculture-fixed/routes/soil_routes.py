from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import db
from database.models import SoilAnalysis
from services.soil_service import analyze_soil

soil_bp = Blueprint('soil', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@soil_bp.route('/', methods=['GET'])
@login_required
def soil_page():
    history = SoilAnalysis.query.filter_by(user_id=session['user_id']).order_by(
        SoilAnalysis.created_at.desc()).limit(10).all()
    return render_template('soil.html', history=[h.to_dict() for h in history])

@soil_bp.route('/analyze', methods=['POST'])
@login_required
def soil_analysis():
    data = request.form if request.form else request.get_json()
    params = {
        'ph': float(data.get('ph', 7.0)),
        'moisture': float(data.get('moisture', 50.0)),
        'nitrogen': float(data.get('nitrogen', 0)),
        'phosphorus': float(data.get('phosphorus', 0)),
        'potassium': float(data.get('potassium', 0))
    }
    result = analyze_soil(params)

    record = SoilAnalysis(
        user_id=session['user_id'],
        ph=params['ph'],
        moisture=params['moisture'],
        nitrogen=params['nitrogen'],
        phosphorus=params['phosphorus'],
        potassium=params['potassium'],
        result=result['quality'],
        recommended_crops=', '.join(result['recommended_crops'])
    )
    db.session.add(record)
    db.session.commit()

    return jsonify(result)

@soil_bp.route('/history', methods=['GET'])
@login_required
def soil_history():
    records = SoilAnalysis.query.filter_by(user_id=session['user_id']).order_by(
        SoilAnalysis.created_at.desc()).all()
    return jsonify([r.to_dict() for r in records])
