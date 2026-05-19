from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.models import LandRegistry
from database.db import db

registry_bp = Blueprint('registry', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@registry_bp.route('/', methods=['GET'])
@login_required
def registry_page():
    """Render the land registry search page"""
    from utils.translator import get_all_translations, SUPPORTED_LANGUAGES
    lang = session.get('language', 'en')
    t = get_all_translations(lang)
    return render_template('registry.html', t=t, lang=lang,
                           languages=SUPPORTED_LANGUAGES)


@registry_bp.route('/search', methods=['GET'])
@login_required
def search_registry():
    """
    Search land registry records.
    Query params: state, city, khata_no, khesra_no, owner_name, land_type
    Pagination:   page (default 1), per_page (default 15, max 50)
    """
    state      = request.args.get('state', '').strip()
    city       = request.args.get('city', '').strip()
    khata_no   = request.args.get('khata_no', '').strip()
    khesra_no  = request.args.get('khesra_no', '').strip()
    owner_name = request.args.get('owner_name', '').strip()
    land_type  = request.args.get('land_type', '').strip()
    page       = max(1, int(request.args.get('page', 1)))
    per_page   = min(50, max(1, int(request.args.get('per_page', 15))))

    q = LandRegistry.query

    if state:      q = q.filter(LandRegistry.state == state)
    if city:       q = q.filter(LandRegistry.city == city)
    if khata_no:   q = q.filter(LandRegistry.khata_no.ilike(f'%{khata_no}%'))
    if khesra_no:  q = q.filter(LandRegistry.khesra_no.ilike(f'%{khesra_no}%'))
    if owner_name: q = q.filter(LandRegistry.owner_name.ilike(f'%{owner_name}%'))
    if land_type:  q = q.filter(LandRegistry.land_type == land_type)

    total   = q.count()
    records = q.offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        'total':       total,
        'page':        page,
        'per_page':    per_page,
        'total_pages': (total + per_page - 1) // per_page,
        'records':     [r.to_dict() for r in records]
    })


@registry_bp.route('/detail/<int:record_id>', methods=['GET'])
@login_required
def record_detail(record_id):
    """Get full detail of one land registry record"""
    r = LandRegistry.query.get_or_404(record_id)
    return jsonify(r.to_dict())


@registry_bp.route('/states', methods=['GET'])
@login_required
def get_states():
    """Return distinct states in the registry"""
    states = db.session.query(LandRegistry.state).distinct().order_by(LandRegistry.state).all()
    return jsonify([s[0] for s in states])


@registry_bp.route('/cities', methods=['GET'])
@login_required
def get_cities():
    """Return cities, optionally filtered by state"""
    state = request.args.get('state', '').strip()
    q = db.session.query(LandRegistry.city).distinct()
    if state:
        q = q.filter(LandRegistry.state == state)
    cities = q.order_by(LandRegistry.city).all()
    return jsonify([c[0] for c in cities])