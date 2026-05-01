from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from database.db import db
from database.models import User
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    data = request.form if request.form else request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    language = data.get('language', 'en')

    if not all([name, email, password]):
        flash('All fields are required.', 'error')
        return render_template('register.html', error='All fields required')

    existing = User.query.filter_by(email=email).first()
    if existing:
        flash('Email already registered.', 'error')
        return render_template('register.html', error='Email already exists')

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(name=name, email=email, password=hashed_pw, language=language)
    db.session.add(user)
    db.session.commit()

    flash('Registration successful! Please login.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.form if request.form else request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        flash('Invalid email or password.', 'error')
        return render_template('login.html', error='Invalid credentials')

    session['user_id'] = user.user_id
    session['user_name'] = user.name
    session['language'] = user.language
    return redirect(url_for('dashboard'))


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@auth_bp.route('/profile', methods=['GET', 'PUT'])
def profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(session['user_id'])
    if request.method == 'GET':
        return jsonify({'name': user.name, 'email': user.email, 'language': user.language})

    data = request.get_json()
    if data.get('language'):
        user.language = data['language']
        session['language'] = data['language']
    db.session.commit()
    return jsonify({'message': 'Profile updated'})
