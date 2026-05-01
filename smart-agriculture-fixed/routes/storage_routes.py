from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for

storage_bp = Blueprint('storage', __name__)

STORAGE_DATA = {
    'wheat': {
        'name': 'Wheat',
        'temperature': '15-25°C',
        'humidity': '50-60%',
        'duration': 'Up to 12 months',
        'method': 'Store in cool, dry place in sealed bags or silos. Use hermetic storage.',
        'tips': [
            'Clean grain before storage to remove impurities',
            'Maintain moisture content below 12%',
            'Use fumigation if needed to prevent pests',
            'Regular inspection every 2-4 weeks'
        ]
    },
    'rice': {
        'name': 'Rice',
        'temperature': '10-20°C',
        'humidity': '60-70%',
        'duration': 'Up to 18 months',
        'method': 'Store in airtight containers or hermetic bags away from direct sunlight.',
        'tips': [
            'Dry properly to 14% moisture before storage',
            'Avoid mixing with old stock (FIFO)',
            'Use neem leaves as natural pest repellent',
            'Check regularly for mold or insect activity'
        ]
    },
    'maize': {
        'name': 'Maize (Corn)',
        'temperature': '10-20°C',
        'humidity': '55-65%',
        'duration': 'Up to 9 months',
        'method': 'Shell and dry before storage. Store in sacks or cribs with ventilation.',
        'tips': [
            'Reduce moisture content to below 13% before storage',
            'Protect from weevils using approved pesticides',
            'Avoid storing on damp floors',
            'Use raised wooden platforms for bags'
        ]
    },
    'pulses': {
        'name': 'Pulses (Dal)',
        'temperature': '15-25°C',
        'humidity': '50-60%',
        'duration': 'Up to 12 months',
        'method': 'Store in airtight containers. Dry thoroughly before storage.',
        'tips': [
            'Mix with a little edible oil (groundnut/castor) to prevent weevils',
            'Store in dark, cool locations',
            'Regular inspection for moisture and pests',
            'Avoid mixing different varieties'
        ]
    },
    'vegetables': {
        'name': 'Vegetables',
        'temperature': '0-10°C',
        'humidity': '85-95%',
        'duration': '1-4 weeks',
        'method': 'Cold chain storage recommended. Use refrigeration or cool storage rooms.',
        'tips': [
            'Harvest at right maturity stage',
            'Avoid bruising during handling',
            'Pre-cool before storage',
            'Sort and remove damaged produce before storing'
        ]
    },
    'fruits': {
        'name': 'Fruits',
        'temperature': '0-15°C',
        'humidity': '85-95%',
        'duration': '1-8 weeks (varies)',
        'method': 'Use cold storage or controlled atmosphere storage for longer life.',
        'tips': [
            'Harvest early morning to reduce field heat',
            'Handle gently to prevent bruising',
            'Use ethylene inhibitors for ripening control',
            'Store separately from vegetables if possible'
        ]
    }
}

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@storage_bp.route('/', methods=['GET'])
@login_required
def storage_page():
    return render_template('storage.html', crops=list(STORAGE_DATA.keys()))

@storage_bp.route('/info', methods=['GET'])
@login_required
def storage_info():
    crop = request.args.get('crop', '').lower()
    if crop in STORAGE_DATA:
        return jsonify(STORAGE_DATA[crop])
    return jsonify({'crops': list(STORAGE_DATA.keys()), 'all': STORAGE_DATA})

@storage_bp.route('/all', methods=['GET'])
@login_required
def all_storage():
    return jsonify(STORAGE_DATA)
