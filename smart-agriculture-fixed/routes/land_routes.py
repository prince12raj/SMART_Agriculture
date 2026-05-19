from flask import (Blueprint, request, jsonify, render_template,
                   session, redirect, url_for, current_app)
from database.db import db
from database.models import LandRecord, LandAnalysis
from utils.preprocess import allowed_file
from services.land_analysis_service import analyze_land_image
from utils.translator import get_all_translations, SUPPORTED_LANGUAGES
import os, uuid

land_bp = Blueprint('land', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@land_bp.route('/', methods=['GET'])
@login_required
def land_page():
    lang = session.get('language', 'en')
    t = get_all_translations(lang)
    records = LandRecord.query.filter_by(user_id=session['user_id']).all()
    return render_template('land.html', records=[r.to_dict() for r in records],
                           t=t, lang=lang, languages=SUPPORTED_LANGUAGES)


@land_bp.route('/add', methods=['POST'])
@login_required
def add_land():
    data = request.form if request.form else request.get_json()
    record = LandRecord(
        user_id    = session['user_id'],
        area       = float(data.get('area', 0)),
        location   = data.get('location', ''),
        soil_type  = data.get('soil_type', ''),
        crop_grown = data.get('crop_grown', ''),
        notes      = data.get('notes', '')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Land record added', 'land_id': record.land_id})


@land_bp.route('/update/<int:land_id>', methods=['PUT'])
@login_required
def update_land(land_id):
    record = LandRecord.query.filter_by(
        land_id=land_id, user_id=session['user_id']).first()
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    data = request.get_json()
    for field in ['area', 'location', 'soil_type', 'crop_grown', 'notes']:
        if field in data:
            setattr(record, field, data[field])
    db.session.commit()
    return jsonify({'message': 'Updated successfully'})


@land_bp.route('/delete/<int:land_id>', methods=['DELETE'])
@login_required
def delete_land(land_id):
    record = LandRecord.query.filter_by(
        land_id=land_id, user_id=session['user_id']).first()
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'})


@land_bp.route('/list', methods=['GET'])
@login_required
def list_lands():
    records = LandRecord.query.filter_by(user_id=session['user_id']).all()
    return jsonify([r.to_dict() for r in records])


# ── NEW: AI Land Image Analysis ──────────────────────────────────────────────

@land_bp.route('/analyze-image', methods=['POST'])
@login_required
def analyze_image():
    """Upload land image → Claude AI analysis → save + return result"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Use JPG, PNG or WebP'}), 400

    filename = f"land_{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    result = analyze_land_image(filepath)

    # Save result to DB
    record = LandAnalysis(
        user_id        = session['user_id'],
        image_path     = filename,
        ph             = result.get('ph'),
        nitrogen       = result.get('nitrogen'),
        phosphorus     = result.get('phosphorus'),
        potassium      = result.get('potassium'),
        organic_matter = result.get('organicMatter'),
        moisture       = result.get('moisture'),
        health_score   = result.get('healthScore'),
        quality        = result.get('quality'),
        texture        = result.get('texture'),
        suitable_crops = ', '.join(result.get('suitableCrops', [])),
        fertilizer     = result.get('fertilizer'),
        irrigation     = result.get('irrigation'),
        summary        = result.get('summary'),
    )
    db.session.add(record)
    db.session.commit()

    return jsonify(result)


@land_bp.route('/analysis-history', methods=['GET'])
@login_required
def analysis_history():
    records = LandAnalysis.query.filter_by(
        user_id=session['user_id']
    ).order_by(LandAnalysis.created_at.desc()).limit(10).all()
    return jsonify([r.to_dict() for r in records])