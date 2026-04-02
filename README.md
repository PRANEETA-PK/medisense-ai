# 🏥 MediSense AI — Smart Health Assistant

> **Health Tech Hackathon Prototype** · AI-Powered Symptom Analysis & Health Management

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python) ![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask) ![License](https://img.shields.io/badge/License-MIT-yellow) ![Status](https://img.shields.io/badge/Status-Prototype-orange)

---

## 🌟 Overview

MediSense AI is a full-stack health technology prototype that empowers individuals to make informed health decisions through intelligent symptom analysis, medication management, and health tracking — all from a clean, accessible web interface.

### The Problem We Solve

- **90% of people** search symptoms online on unverified platforms
- **Medication non-adherence** causes ~125,000 deaths annually in the US
- **Early triage** can significantly reduce unnecessary ER visits

MediSense AI addresses all three pain points in a single, unified interface.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🩺 **AI Symptom Checker** | Analyzes symptoms against a curated medical knowledge base. Returns possible conditions, urgency level, and actionable advice |
| ⚖️ **BMI Calculator** | Instant BMI calculation with personalized health insights and visual reference scale |
| 💊 **Medicine Reminders** | Add, manage, and track medication schedules with time-based reminders |
| 📋 **Health History** | All past symptom analyses stored per session for pattern recognition |
| 💡 **Health Tips** | Rotating evidence-based daily health recommendations |

---

## 🏗️ Architecture

```
medisense-ai/
├── app.py                    # Flask backend — routes & business logic
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html            # Single-page HTML template (Jinja2)
└── static/
    ├── css/
    │   └── style.css         # Full responsive stylesheet
    └── js/
        └── app.js            # Frontend logic (vanilla JS)
```

### Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.9+, Flask 3.0 |
| **Frontend** | Vanilla HTML5, CSS3 (custom), JavaScript (ES2022) |
| **Storage** | In-memory (session-based) — upgrade path: SQLite / PostgreSQL |
| **Fonts** | DM Serif Display + DM Sans (Google Fonts) |
| **Deployment** | Gunicorn (production WSGI server) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/PRANEETA-PK/medisense-ai.git
cd medisense-ai

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open your browser at **http://localhost:5000** 🎉

### Production Deployment

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

## 🔬 How It Works

### Symptom Analysis Engine

```
User Input → Text Normalization → Keyword Matching → Knowledge Base Lookup
         → Urgency Ranking → Condition Aggregation → Remedy Compilation
         → Response with Advice
```

The symptom checker uses a **curated knowledge base** with 10 symptom categories covering:
- Respiratory (cough, shortness of breath)
- Cardiovascular (chest pain)
- Neurological (headache, dizziness)
- Systemic (fever, fatigue)
- Gastrointestinal (nausea)
- Dermatological (rash)
- ENT (sore throat)

**Urgency levels:**
- 🟢 **Low** — Self-care appropriate, monitor symptoms
- 🟠 **Moderate** — Consider medical consultation within 24-48 hours
- 🔴 **High** — Seek emergency care immediately

### BMI Calculation

```
BMI = weight(kg) / height(m)²
```

Categorized per WHO standards: Underweight / Normal / Overweight / Obese

---

## 📡 API Reference

### `POST /api/analyze`
Analyze symptoms and return health insights.

**Request Body:**
```json
{
  "symptoms": "fever, headache, cough",
  "age": 28,
  "gender": "female"
}
```

**Response:**
```json
{
  "success": true,
  "matched_symptoms": ["fever", "headache", "cough"],
  "possible_conditions": ["Common Cold", "Influenza", "COVID-19"],
  "urgency": "low",
  "advice": "Stay hydrated and rest...",
  "remedies": ["Paracetamol", "Steam inhalation"],
  "disclaimer": "Not a substitute for professional advice.",
  "timestamp": "2024-01-15T10:30:00"
}
```

### `POST /api/bmi`
Calculate BMI.

**Request:** `{ "weight": 70, "height": 175 }`
**Response:** `{ "bmi": 22.9, "category": "Normal Weight", "advice": "..." }`

### `GET /api/reminders`
Fetch all reminders for current session.

### `POST /api/reminders`
Add a new medicine reminder.

**Request:**
```json
{
  "medicine": "Metformin",
  "dosage": "500mg",
  "time": "08:00",
  "frequency": "daily"
}
```

### `DELETE /api/reminders/<id>`
Delete a specific reminder.

### `GET /api/history`
Fetch all symptom analyses for current session.

### `GET /api/health-tip`
Get a random daily health tip.

---

## 🔮 Future Roadmap

- [ ] **User authentication** (JWT-based accounts)
- [ ] **Database persistence** (PostgreSQL + SQLAlchemy)
- [ ] **Push notifications** for medicine reminders (Web Push API)
- [ ] **Wearable integration** (heart rate, SpO2 data)
- [ ] **ML model** trained on medical datasets for better condition prediction
- [ ] **Multi-language support** (Hindi, Tamil, Telugu)
- [ ] **Telemedicine integration** — book doctor appointments directly
- [ ] **PDF health report** export

---

## ⚠️ Disclaimer

MediSense AI is an **educational prototype** built for a health technology hackathon. It is **not** a licensed medical device and should **not** replace consultation with a qualified healthcare professional. Always seek professional medical advice for health concerns.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👩‍💻 Built By

**PRANEETA-PK** · Health Tech Hackathon 2024

*"Technology in service of better health for everyone."*
