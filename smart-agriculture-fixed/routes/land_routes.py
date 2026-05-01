from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import db
from database.models import LandRecord

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
    records = LandRecord.query.filter_by(user_id=session['user_id']).all()
    return render_template('land.html', records=[r.to_dict() for r in records])

@land_bp.route('/add', methods=['POST'])
@login_required
def add_land():
    data = request.form if request.form else request.get_json()
    record = LandRecord(
        user_id=session['user_id'],
        area=float(data.get('area', 0)),
        location=data.get('location', ''),
        soil_type=data.get('soil_type', ''),
        crop_grown=data.get('crop_grown', ''),
        notes=data.get('notes', '')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Land record added', 'land_id': record.land_id})

@land_bp.route('/update/<int:land_id>', methods=['PUT'])
@login_required
def update_land(land_id):
    record = LandRecord.query.filter_by(land_id=land_id, user_id=session['user_id']).first()
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
    record = LandRecord.query.filter_by(land_id=land_id, user_id=session['user_id']).first()
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
