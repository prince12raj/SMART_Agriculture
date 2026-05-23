<div align="center">

# 🌾 SMART Agriculture
### AI-Powered Farm Management System

![Version](https://img.shields.io/badge/version-2.0.0-2D6A4F?style=for-the-badge&logo=git&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![Claude AI](https://img.shields.io/badge/Claude_AI-Anthropic-D97706?style=for-the-badge&logo=anthropic&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-40916C?style=for-the-badge)

<br/>

> **SMART Agriculture** is an AI-powered farm management platform built for Indian farmers.
> Upload a soil photo, detect crop diseases, predict market prices, and chat with AgriBot — all in your own language.

<br/>

🌐 **[Live Demo](https://smart-agriculture-y8c4.onrender.com)** &nbsp;|&nbsp; ⚙️ **[GitHub](https://github.com/prince12raj/SMART_Agriculture.git)** &nbsp;|&nbsp; 📬 **[Report Issue](https://github.com/prince12raj/SMART_Agriculture/issues)**

</div>

---

## 📸 Dashboard Preview

```
╔══════════════════════════════════════════════════════════════════════╗
║  🌾 AgriSmart                        [Lang ▼]  🔔  👤 Prince Raj   ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║   Good Morning, Prince 👋                                            ║
║   Here's your farm overview for today                                ║
║                                                                      ║
║  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  ║
║  │  🗺️ Land    │ │  🧪 Soil    │ │  🔬 Disease │ │  📈 Prices  │  ║
║  │   Records   │ │  Analyses   │ │   Scans     │ │ Predictions │  ║
║  │    ──       │ │    ──       │ │    ──       │ │    ──       │  ║
║  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘  ║
║                                                                      ║
║   🚀 Quick Access                                                     ║
║  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                ║
║  │ 🗺️ Land      │ │ 🧪 Soil      │ │ 🔬 Disease   │                ║
║  │  Records     │ │  Analysis    │ │  Detection   │                ║
║  │              │ │              │ │              │                ║
║  │ Manage your  │ │ AI soil scan │ │ Upload leaf  │                ║
║  │ land parcels │ │ + crop tips  │ │ → diagnosis  │                ║
║  │  [Open →]   │ │ [Analyze →] │ │  [Detect →] │                ║
║  └──────────────┘ └──────────────┘ └──────────────┘                ║
║                                                                      ║
║  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                ║
║  │ 📈 Prices    │ │ 🏚️ Storage   │ │ 📜 Registry  │                ║
║  │ Prediction   │ │  Guidelines  │ │  Land Lookup │                ║
║  │              │ │              │ │              │                ║
║  │ Predict crop │ │ Storage tips │ │ Search Khata │                ║
║  │ market price │ │ per crop type│ │ & Khesra No. │                ║
║  │ [Predict →] │ │ [View →]    │ │  [Search →] │                ║
║  └──────────────┘ └──────────────┘ └──────────────┘                ║
║                                                                      ║
║                                              🤖 ← AgriBot (always)  ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## ✨ Features

### 🧪 Soil Analysis
- Enter NPK, pH, and moisture values via sliders for instant analysis
- **AI Image Analysis** — upload a soil photo and Claude Vision identifies soil type, texture, health score (0–100), suitable crops, fertilizer plan, irrigation advice, and a seasonal crop calendar (Kharif / Rabi / Zaid)

### 🔬 Crop Disease Detection
- Upload a leaf photo — CNN + Claude Vision identifies disease name, severity, treatment, and organic alternatives
- Actionable prevention steps included

### 📈 Market Price Prediction
- Predict crop market prices based on crop type, season, and region
- Decide the best time to sell and maximize profit

### 🤖 AgriBot — AI Chatbot
- Floating robot button on every page
- Auto-detects **Hindi** and **English** — reply in the same language
- Knows Indian crops, diseases, government schemes (PM-KISAN, soil health card), mandi prices, and weather tips
- Conversation memory within the session

### 🗺️ Land Records
- Add and manage land parcels with location, area, and soil type
- View all records in a clean dashboard

### 📜 Land Registry
- Search government land records by Khata No. and Khesra No.
- Multilingual support for all registry data

### 🏚️ Grain Storage
- Storage temperature, humidity, and duration guidelines per crop
- Best practices for post-harvest storage

### 🌍 Multi-Language Support
| Language | Script | Region |
|---|---|---|
| Hindi | हिंदी | North India |
| English | English | All India |
| Punjabi | ਪੰਜਾਬੀ | Punjab, Haryana |
| Marathi | मराठी | Maharashtra |
| Telugu | తెలుగు | Andhra, Telangana |
| Gujarati | ગુજરાતી | Gujarat |

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript, Jinja2 Templates |
| **Backend** | Python 3.11, Flask 3.0, Flask-SQLAlchemy, Flask-Migrate, Bcrypt |
| **AI / ML** | Anthropic Claude API (Vision + Chat), CNN (TensorFlow/Keras), Pillow, NumPy |
| **Database** | PostgreSQL, SQLAlchemy ORM |
| **Auth** | Flask session-based auth, Bcrypt password hashing |
| **Deployment** | Render.com, Gunicorn, GitHub, python-dotenv |

---

## 🧠 CNN Architecture — Disease Detection

```
Input Layer          →  224 × 224 × 3 RGB Image
Conv2D (32 filters)  →  3×3 kernel · ReLU activation
MaxPooling2D         →  2×2 pool · Stride 2
Conv2D (64 filters)  →  3×3 kernel · ReLU activation
MaxPooling2D         →  2×2 pool · Stride 2
Conv2D (128 filters) →  3×3 kernel · ReLU activation
MaxPooling2D         →  2×2 pool · Stride 2
Flatten              →  Converts feature maps to 1D vector
Dense (256 units)    →  Fully Connected · ReLU
Dropout (0.5)        →  Regularization to prevent overfitting
Output (Softmax)     →  N disease classes
```

---

## 🔌 API Usage

### Claude Vision — Soil Image Analysis
```python
# POST /soil/analyze-image
# Model: claude-opus-4-5
# Returns: soil_type, ph_estimate, npk_levels, health_score,
#          suitable_crops, fertilizer_recommendations, season_calendar
```

### Claude Chat — AgriBot
```python
# POST /chatbot/chat
# Model: claude-sonnet-4-20250514
# Auto-detects Hindi / English from user message
# System prompt: Indian farming expert context
```

### Claude Vision — Disease Detection
```python
# POST /disease/analyze
# Model: claude-opus-4-5
# Returns: disease_name, severity, treatment, prevention, organic_alternatives
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL
- Anthropic API key → [console.anthropic.com](https://console.anthropic.com/settings/keys)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/prince12raj/SMART_Agriculture.git
cd SMART_Agriculture/smart-agriculture-fixed

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env and add your values
```

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/smart_agriculture
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxx
UPLOAD_FOLDER=uploads
FLASK_ENV=development
```

### Run Locally

```bash
# Initialize database
flask db upgrade

# Start the server
python app.py
```

Open `http://localhost:5000` in your browser.

---

## 📁 Project Structure

```
smart-agriculture-fixed/
│
├── app.py                        # Flask app entry point
├── config.py                     # Configuration settings
├── requirements.txt              # Python dependencies
│
├── routes/
│   ├── auth_routes.py            # Login, Register, Logout
│   ├── soil_routes.py            # Soil analysis + image AI
│   ├── disease_routes.py         # Disease detection
│   ├── land_routes.py            # Land records management
│   ├── price_routes.py           # Price prediction
│   ├── storage_routes.py         # Storage guidelines
│   ├── registry_routes.py        # Land registry search
│   └── chatbot_routes.py         # AgriBot AI chat
│
├── services/
│   ├── soil_service.py           # Manual soil analysis logic
│   ├── soil_image_service.py     # Claude Vision soil analysis
│   └── disease_service.py        # Disease detection logic
│
├── database/
│   ├── db.py                     # SQLAlchemy instance
│   └── models.py                 # User, SoilAnalysis, Land models
│
├── templates/                    # Jinja2 HTML templates
│   ├── dashboard.html
│   ├── soil.html
│   ├── disease.html
│   ├── land.html
│   ├── price.html
│   ├── storage.html
│   ├── registry.html
│   ├── login.html
│   └── register.html
│
├── static/
│   ├── css/style.css             # Global styles + CSS variables
│   └── js/
│       ├── script.js             # Global scripts
│       ├── chatbot.js            # AgriBot floating widget
│       └── land_analysis.js      # Land page scripts
│
└── utils/
    └── translator.py             # Multi-language translation utility
```

---

## 🌐 Deployment on Render

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service → Connect your repo
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `gunicorn app:app`
5. Add Environment Variables:
   - `ANTHROPIC_API_KEY` → your key from console.anthropic.com
   - `DATABASE_URL` → your PostgreSQL URL
   - `SECRET_KEY` → any random secret string

The app auto-deploys on every `git push` to main.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

```bash
# Fork → clone → create branch → commit → push → PR
git checkout -b feature/your-feature-name
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
```

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

## 👨‍💻 Authors

<table>
  <tr>
    <td align="center">
      <b>Prince Raj</b><br/>
      <sub>Full Stack & AI Developer</sub><br/>
      <a href="https://github.com/prince12raj">@prince12raj</a>
    </td>
    <td align="center">
      <b>Priyam Mishra</b><br/>
      <sub>Backend & ML Engineer</sub><br/>
      <a href="https://github.com/priyam12mishra">@priyam12mishra</a>
    </td>
  </tr>
</table>

<br/>

**© 2026 Prince Raj & Priyam Mishra — SMART Agriculture**

*Built with ❤️ for Indian Farmers*

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Visit_Now-2D6A4F?style=for-the-badge)](https://smart-agriculture-y8c4.onrender.com)
[![GitHub](https://img.shields.io/badge/⚙️_GitHub-View_Code-181717?style=for-the-badge&logo=github)](https://github.com/prince12raj/SMART_Agriculture.git)

</div>
