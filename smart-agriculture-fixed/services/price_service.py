import os
try:
    import joblib
    import numpy as np
    HAS_ML = True
except ImportError:
    import random
    HAS_ML = False

# Base prices per quintal (INR) - historical averages
BASE_PRICES = {
    'wheat': 2200, 'rice': 2500, 'maize': 1900, 'cotton': 6500,
    'sugarcane': 350, 'soybean': 4200, 'groundnut': 5800, 'potato': 1200,
    'onion': 1500, 'tomato': 1800, 'mustard': 5400, 'barley': 1850,
    'pulses': 6000, 'jowar': 2900, 'bajra': 2250, 'turmeric': 12000
}

# Seasonal multipliers (month 1-12)
SEASONAL_FACTORS = {
    'wheat': [1.1, 1.05, 0.95, 0.9, 1.0, 1.05, 1.1, 1.1, 1.05, 1.0, 0.95, 1.0],
    'rice': [1.0, 1.0, 1.05, 1.1, 1.1, 1.0, 0.95, 0.9, 0.95, 1.0, 1.05, 1.05],
    'default': [1.0] * 12
}

# State-wise multipliers
STATE_FACTORS = {
    'punjab': 0.95, 'haryana': 0.97, 'uttar pradesh': 1.0,
    'maharashtra': 1.05, 'karnataka': 1.08, 'andhra pradesh': 1.02,
    'madhya pradesh': 0.98, 'rajasthan': 1.03, 'gujarat': 1.06,
    'west bengal': 1.01, 'bihar': 1.04, 'default': 1.0
}

def predict_price(crop_name, state, market, month):
    """
    Predict crop price using ML model or heuristic system.
    Returns predicted price per quintal in INR.
    """
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'price_model.pkl')

    if HAS_ML and os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            # Encode features as needed by your trained model
            features = _encode_features(crop_name, state, market, month)
            price = float(model.predict([features])[0])
            return _format_result(crop_name, state, price, month)
        except Exception:
            pass

    return _heuristic_price(crop_name, state, market, month)

def _heuristic_price(crop_name, state, market, month):
    crop_key = crop_name.lower().strip()
    base = BASE_PRICES.get(crop_key, 2000)

    seasonal = SEASONAL_FACTORS.get(crop_key, SEASONAL_FACTORS['default'])
    month_idx = max(0, min(11, (month or 1) - 1))
    seasonal_factor = seasonal[month_idx]

    state_key = state.lower().strip() if state else 'default'
    state_factor = STATE_FACTORS.get(state_key, STATE_FACTORS['default'])

    price = base * seasonal_factor * state_factor
    if HAS_ML:
        noise = np.random.uniform(-0.03, 0.03)
    else:
        import random
        noise = random.uniform(-0.03, 0.03)
    price = price * (1 + noise)

    return _format_result(crop_name, state, price, month)

def _format_result(crop_name, state, price, month):
    import calendar
    month_name = calendar.month_name[max(1, min(12, month or 1))]
    trend = 'Rising' if price > BASE_PRICES.get(crop_name.lower(), 2000) else 'Stable'
    return {
        'crop': crop_name,
        'state': state,
        'month': month_name,
        'price': round(price, 2),
        'unit': 'per quintal (INR)',
        'trend': trend,
        'recommendation': _get_recommendation(price, crop_name)
    }

def _get_recommendation(price, crop_name):
    base = BASE_PRICES.get(crop_name.lower(), 2000)
    if price > base * 1.1:
        return 'Good time to sell — prices are above average.'
    elif price < base * 0.9:
        return 'Hold if possible — prices are below average. Consider storage.'
    else:
        return 'Prices are near average. Sell based on storage costs and urgency.'

def _encode_features(crop_name, state, market, month):
    # Placeholder feature encoding for ML model
    return [hash(crop_name) % 100, hash(state) % 50, hash(market) % 50, month or 1]
