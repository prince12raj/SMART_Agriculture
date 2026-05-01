from flask import Flask, render_template, redirect, url_for, session
from config import Config
from database.db import init_db
from routes.auth_routes import auth_bp
from routes.land_routes import land_bp
from routes.soil_routes import soil_bp
from routes.disease_routes import disease_bp
from routes.price_routes import price_bp
from routes.storage_routes import storage_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(land_bp, url_prefix='/land')
app.register_blueprint(soil_bp, url_prefix='/soil')
app.register_blueprint(disease_bp, url_prefix='/disease')
app.register_blueprint(price_bp, url_prefix='/price')
app.register_blueprint(storage_bp, url_prefix='/storage')

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

# Initialize DB
init_db(app)

if __name__ == '__main__':
    app.run(debug=True)
