from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, current_app
from database.db import db
from database.models import CropDisease
from services.disease_service import detect_disease
from utils.preprocess import allowed_file
import os, uuid

disease_bp = Blueprint('disease', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@disease_bp.route('/', methods=['GET'])
@login_required
def disease_page():
    history = CropDisease.query.filter_by(user_id=session['user_id']).order_by(
        CropDisease.created_at.desc()).limit(10).all()
    return render_template('disease.html', history=[h.to_dict() for h in history])

@disease_bp.route('/detect', methods=['POST'])
@login_required
def disease_detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    crop_name = request.form.get('crop_name', 'Unknown')

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    result = detect_disease(filepath, crop_name)

    record = CropDisease(
        user_id=session['user_id'],
        image_path=filename,
        crop_name=crop_name,
        prediction=result['disease'],
        solution=result['solution'],
        confidence=result['confidence']
    )
    db.session.add(record)
    db.session.commit()

    return jsonify(result)

@disease_bp.route('/history', methods=['GET'])
@login_required
def disease_history():
    records = CropDisease.query.filter_by(user_id=session['user_id']).order_by(
        CropDisease.created_at.desc()).all()
    return jsonify([r.to_dict() for r in records])
