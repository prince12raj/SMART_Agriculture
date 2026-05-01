# 🌾 AgriSmart — Smart Agriculture Management System

A multi-functional web-based platform designed to support farmers with digital tools for land management, soil analysis, crop disease detection, price prediction, and grain storage guidance.

---

## 🚀 Quick Start

### 1. Clone / Download the project
```bash
cd smart-agriculture-system
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

Visit: **http://localhost:5000**

---

## 🧩 System Modules

| Module | Route | Description |
|--------|-------|-------------|
| Authentication | `/auth/` | Register, login, logout |
| Land Records | `/land/` | Add/view/delete land parcels |
| Soil Analysis | `/soil/` | ML-based soil quality analysis |
| Disease Detection | `/disease/` | AI crop disease detection from images |
| Price Prediction | `/price/` | Crop market price forecasting |
| Grain Storage | `/storage/` | Storage guidelines per crop |

---

## 🏗️ Project Structure

```
smart-agriculture-system/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── templates/              # HTML templates
│   ├── index.html          # Landing page
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── land.html
│   ├── soil.html
│   ├── disease.html
│   ├── price.html
│   └── storage.html
│
├── static/
│   ├── css/style.css       # Main stylesheet
│   └── js/script.js        # Frontend JavaScript
│
├── routes/                 # Flask Blueprints
│   ├── auth_routes.py
│   ├── land_routes.py
│   ├── soil_routes.py
│   ├── disease_routes.py
│   ├── price_routes.py
│   └── storage_routes.py
│
├── services/               # Business logic
│   ├── soil_service.py
│   ├── disease_service.py
│   └── price_service.py
│
├── database/
│   ├── db.py               # DB connection (SQLAlchemy)
│   └── models.py           # Table definitions
│
├── utils/
│   ├── preprocess.py       # Image & data utilities
│   └── translator.py       # Multi-language support
│
├── models/                 # Trained ML models (place here)
│   ├── soil_model.pkl
│   ├── disease_model.h5
│   └── price_model.pkl
│
├── datasets/               # Training datasets (optional)
└── uploads/                # Uploaded crop images
```

---

## 🧠 ML Models

The system uses three ML models. Place pre-trained models in the `/models/` folder:

| File | Purpose | Format |
|------|---------|--------|
| `soil_model.pkl` | Soil quality classification | scikit-learn pickle |
| `disease_model.h5` | Crop disease detection | TensorFlow/Keras H5 |
| `price_model.pkl` | Crop price regression | scikit-learn pickle |

**Without models:** The system falls back to a rule-based analysis system, so it works out of the box.

### Training your own models
1. Download datasets from Kaggle:
   - Soil: [Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
   - Disease: [Plant Village Dataset](https://www.kaggle.com/datasets/emmarex/plantdisease)
   - Prices: [Crop Price Dataset](https://www.kaggle.com/datasets/kianwee/agricultural-raw-material-prices-1990-2020)

2. Train and save models to `/models/` directory

---

## 🗄️ Database

By default the app uses **SQLite** (`agri.db`). To use MySQL/PostgreSQL, update `config.py`:

```python
DATABASE_URI = 'mysql+pymysql://user:password@localhost/agridb'
# or
DATABASE_URI = 'postgresql://user:password@localhost/agridb'
```

Tables created automatically on first run:
- `users` — User accounts
- `land_records` — Land parcel records
- `soil_analysis` — Soil test history
- `crop_diseases` — Disease scan history
- `price_predictions` — Price prediction history

---

## 🌍 Multi-language Support

Supported languages:
- English (`en`)
- Hindi / हिंदी (`hi`)
- Punjabi / ਪੰਜਾਬੀ (`pa`)
- Marathi / मराठी (`mr`)
- Telugu / తెలుగు (`te`)

To add a language, edit `utils/translator.py` and add translations to the `TRANSLATIONS` dict.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | User registration |
| POST | `/auth/login` | User login |
| GET | `/auth/logout` | Logout |
| GET/POST | `/land/` | Land records page |
| POST | `/land/add` | Add land record |
| DELETE | `/land/delete/<id>` | Delete land record |
| GET/POST | `/soil/` | Soil analysis page |
| POST | `/soil/analyze` | Run soil analysis |
| GET/POST | `/disease/` | Disease detection page |
| POST | `/disease/detect` | Detect crop disease |
| GET/POST | `/price/` | Price prediction page |
| POST | `/price/predict` | Predict crop price |
| GET | `/storage/` | Storage guidance page |
| GET | `/storage/info?crop=wheat` | Get storage info for crop |

---

## 📈 Future Enhancements

- [ ] Mobile app (React Native / Flutter)
- [ ] Weather API integration (OpenWeatherMap)
- [ ] IoT soil sensor integration
- [ ] Government scheme recommendations
- [ ] SMS alerts for price changes
- [ ] Crop calendar and planting reminders
- [ ] Market connections (buyer-seller platform)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Backend | Python 3.10+, Flask 3.0 |
| Database | SQLite / MySQL / PostgreSQL (SQLAlchemy ORM) |
| ML/AI | scikit-learn, TensorFlow/Keras, Pandas, NumPy |
| Auth | bcrypt password hashing, Flask sessions |

---

## 📄 License

MIT License — Free to use, modify, and distribute.

---

Built with 💚 for Indian Farmers | AgriSmart 2024
