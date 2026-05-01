from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import db
from database.models import PricePrediction
from services.price_service import predict_price

price_bp = Blueprint('price', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@price_bp.route('/', methods=['GET'])
@login_required
def price_page():
    history = PricePrediction.query.order_by(PricePrediction.date.desc()).limit(10).all()
    return render_template('price.html', history=[h.to_dict() for h in history])

@price_bp.route('/predict', methods=['POST'])
@login_required
def price_predict():
    data = request.form if request.form else request.get_json()
    crop_name = data.get('crop_name', '')
    state = data.get('state', '')
    market = data.get('market', '')
    month = int(data.get('month', 1))

    result = predict_price(crop_name, state, market, month)

    record = PricePrediction(
        crop_name=crop_name,
        state=state,
        market=market,
        predicted_price=result['price'],
        unit='quintal'
    )
    db.session.add(record)
    db.session.commit()

    return jsonify(result)

@price_bp.route('/history', methods=['GET'])
@login_required
def price_history():
    records = PricePrediction.query.order_by(PricePrediction.date.desc()).limit(20).all()
    return jsonify([r.to_dict() for r in records])
