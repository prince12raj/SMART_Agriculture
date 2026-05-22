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


import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from services.soil_image_service import analyze_soil_image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@soil_bp.route('/analyze-image', methods=['POST'])
@login_required
def soil_image_analysis():
    """Analyze soil quality from an uploaded image using Claude Vision API."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Use JPG, PNG, or WebP.'}), 400

    # Save to uploads folder
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    ext = os.path.splitext(secure_filename(file.filename))[1].lower()
    unique_name = f"soil_{session['user_id']}_{uuid.uuid4().hex[:8]}{ext}"
    save_path = os.path.join(upload_folder, unique_name)
    file.save(save_path)

    # Run AI analysis
    result = analyze_soil_image(save_path)

    # Clean up temp file
    try:
        os.remove(save_path)
    except Exception:
        pass

    if 'error' in result and not result.get('success'):
        return jsonify(result), 500

    # Save a summary record to DB
    try:
        quality = result.get('quality', 'Unknown')
        crops = result.get('suitable_crops', [])
        record = SoilAnalysis(
            user_id=session['user_id'],
            ph=result.get('ph_estimate', 7.0),
            moisture=result.get('moisture_estimate', 50.0),
            nitrogen=0,
            phosphorus=0,
            potassium=0,
            result=f"[Image] {quality}",
            recommended_crops=', '.join(crops[:6]) if crops else ''
        )
        db.session.add(record)
        db.session.commit()
    except Exception:
        pass  # Non-critical

    return jsonify(result)
