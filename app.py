"""
MediSense AI - Smart Health Assistant
A Flask-based health tech prototype with AI-powered symptom analysis,
medicine reminders, and health history tracking.
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import json
import uuid
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "medisense-dev-secret-2024")

# ─── Symptom-Condition Knowledge Base ────────────────────────────────────────
SYMPTOM_DB = {
    "fever": {
        "conditions": ["Common Cold", "Influenza", "COVID-19", "Bacterial Infection"],
        "urgency": "moderate",
        "advice": "Stay hydrated, rest well. Seek immediate care if temperature exceeds 103°F (39.4°C).",
        "remedies": ["Paracetamol / Acetaminophen", "Plenty of fluids", "Rest", "Lukewarm compress"],
    },
    "headache": {
        "conditions": ["Tension Headache", "Migraine", "Dehydration", "Sinusitis"],
        "urgency": "low",
        "advice": "Rest in a dark, quiet room. Sudden severe headache warrants emergency care.",
        "remedies": ["Ibuprofen / Paracetamol", "Hydration", "Cold/warm compress", "Rest"],
    },
    "cough": {
        "conditions": ["Common Cold", "Bronchitis", "Asthma", "COVID-19", "Allergies"],
        "urgency": "low",
        "advice": "Steam inhalation helps. Persistent cough over 3 weeks needs medical evaluation.",
        "remedies": ["Honey & ginger tea", "Steam inhalation", "Throat lozenges", "Humidifier"],
    },
    "chest pain": {
        "conditions": ["Angina", "Heart Attack", "GERD", "Costochondritis", "Anxiety"],
        "urgency": "high",
        "advice": "⚠️ SEEK EMERGENCY CARE IMMEDIATELY if accompanied by shortness of breath or left arm pain.",
        "remedies": ["Call emergency services immediately", "Do not drive yourself", "Chew aspirin if not allergic (325mg)"],
    },
    "fatigue": {
        "conditions": ["Anemia", "Hypothyroidism", "Depression", "Diabetes", "Sleep Disorder"],
        "urgency": "low",
        "advice": "Maintain regular sleep schedule. Persistent fatigue lasting weeks needs blood work.",
        "remedies": ["Improve sleep hygiene", "B12 / Iron supplements (if deficient)", "Light exercise", "Stress management"],
    },
    "nausea": {
        "conditions": ["Gastroenteritis", "Food Poisoning", "Motion Sickness", "Pregnancy"],
        "urgency": "low",
        "advice": "Stay hydrated with small sips. Seek care if unable to keep fluids down for 24+ hours.",
        "remedies": ["Ginger tea", "BRAT diet", "ORS solution", "Rest"],
    },
    "shortness of breath": {
        "conditions": ["Asthma", "Pneumonia", "Heart Failure", "Anxiety", "Anemia"],
        "urgency": "high",
        "advice": "⚠️ This requires urgent medical evaluation. Call emergency services if severe.",
        "remedies": ["Sit upright", "Use prescribed inhaler if available", "Seek immediate care"],
    },
    "dizziness": {
        "conditions": ["Vertigo", "Low Blood Pressure", "Dehydration", "Anemia", "Inner Ear Issue"],
        "urgency": "moderate",
        "advice": "Sit or lie down immediately to prevent falls. Recurring dizziness needs evaluation.",
        "remedies": ["Hydration", "Slow positional changes", "Rest", "Ginger"],
    },
    "rash": {
        "conditions": ["Allergic Reaction", "Eczema", "Contact Dermatitis", "Viral Infection"],
        "urgency": "moderate",
        "advice": "Avoid scratching. Widespread rash with fever or difficulty breathing needs emergency care.",
        "remedies": ["Antihistamines", "Calamine lotion", "Cool compress", "Avoid irritants"],
    },
    "sore throat": {
        "conditions": ["Strep Throat", "Viral Pharyngitis", "Tonsillitis", "Acid Reflux"],
        "urgency": "low",
        "advice": "Gargle warm salt water. White patches or high fever may indicate strep — see a doctor.",
        "remedies": ["Warm salt gargle", "Honey & lemon", "Throat lozenges", "Paracetamol"],
    },
}

HEALTH_TIPS = [
    "💧 Drink at least 8 glasses of water daily",
    "🚶 Walk 30 minutes every day to boost cardiovascular health",
    "😴 Adults need 7–9 hours of quality sleep per night",
    "🥗 Eat 5 portions of fruits and vegetables daily",
    "🧘 Practice mindfulness — even 5 minutes reduces stress significantly",
    "☀️ Get 15–20 mins of sunlight daily for Vitamin D",
    "🦷 Brush twice daily — oral health directly impacts heart health",
    "📵 Limit screen time 1 hour before bed for better sleep quality",
]

# ─── In-memory storage (replace with DB in production) ────────────────────────
health_records = {}
reminders = {}


@app.route("/")
def index():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze_symptoms():
    data = request.get_json()
    symptoms_input = data.get("symptoms", "").lower()
    age = data.get("age", 30)
    gender = data.get("gender", "unknown")

    matched = {}
    words = symptoms_input.replace(",", " ").split()
    
    # Multi-word symptom matching
    for symptom_key in SYMPTOM_DB:
        if symptom_key in symptoms_input:
            matched[symptom_key] = SYMPTOM_DB[symptom_key]

    # Single word matching as fallback
    if not matched:
        for word in words:
            for symptom_key in SYMPTOM_DB:
                if word in symptom_key or symptom_key in word:
                    matched[symptom_key] = SYMPTOM_DB[symptom_key]

    if not matched:
        return jsonify({
            "success": False,
            "message": "No recognizable symptoms found. Please try keywords like: fever, headache, cough, chest pain, fatigue, nausea, dizziness, rash, sore throat.",
        })

    # Determine overall urgency
    urgency_rank = {"high": 3, "moderate": 2, "low": 1}
    max_urgency = max(matched.values(), key=lambda x: urgency_rank.get(x["urgency"], 0))

    all_conditions = list({c for s in matched.values() for c in s["conditions"]})[:6]
    all_remedies = list({r for s in matched.values() for r in s["remedies"]})[:6]

    result = {
        "success": True,
        "matched_symptoms": list(matched.keys()),
        "possible_conditions": all_conditions,
        "urgency": max_urgency["urgency"],
        "advice": max_urgency["advice"],
        "remedies": all_remedies,
        "disclaimer": "This is not a substitute for professional medical advice. Always consult a qualified healthcare provider.",
        "timestamp": datetime.now().isoformat(),
    }

    # Save to health history
    user_id = session.get("user_id", "anonymous")
    if user_id not in health_records:
        health_records[user_id] = []
    health_records[user_id].append({
        "symptoms": symptoms_input,
        "age": age,
        "gender": gender,
        "result": result,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })

    return jsonify(result)


@app.route("/api/reminders", methods=["GET"])
def get_reminders():
    user_id = session.get("user_id", "anonymous")
    return jsonify({"reminders": reminders.get(user_id, [])})


@app.route("/api/reminders", methods=["POST"])
def add_reminder():
    data = request.get_json()
    user_id = session.get("user_id", "anonymous")
    if user_id not in reminders:
        reminders[user_id] = []

    reminder = {
        "id": str(uuid.uuid4())[:8],
        "medicine": data.get("medicine", ""),
        "dosage": data.get("dosage", ""),
        "time": data.get("time", ""),
        "frequency": data.get("frequency", "daily"),
        "created": datetime.now().strftime("%Y-%m-%d"),
    }
    reminders[user_id].append(reminder)
    return jsonify({"success": True, "reminder": reminder})


@app.route("/api/reminders/<reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):
    user_id = session.get("user_id", "anonymous")
    if user_id in reminders:
        reminders[user_id] = [r for r in reminders[user_id] if r["id"] != reminder_id]
    return jsonify({"success": True})


@app.route("/api/history", methods=["GET"])
def get_history():
    user_id = session.get("user_id", "anonymous")
    return jsonify({"history": health_records.get(user_id, [])})


@app.route("/api/health-tip", methods=["GET"])
def health_tip():
    import random
    return jsonify({"tip": random.choice(HEALTH_TIPS)})


@app.route("/api/bmi", methods=["POST"])
def calculate_bmi():
    data = request.get_json()
    weight = float(data.get("weight", 0))  # kg
    height = float(data.get("height", 0))  # cm

    if weight <= 0 or height <= 0:
        return jsonify({"success": False, "message": "Invalid input"})

    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 1)

    if bmi < 18.5:
        category = "Underweight"
        color = "blue"
        advice = "Consider a nutrient-rich diet and consult a dietitian."
    elif bmi < 25:
        category = "Normal Weight"
        color = "green"
        advice = "Great! Maintain your healthy lifestyle."
    elif bmi < 30:
        category = "Overweight"
        color = "orange"
        advice = "Regular exercise and balanced diet can help."
    else:
        category = "Obese"
        color = "red"
        advice = "Please consult a healthcare provider for a personalized plan."

    return jsonify({
        "success": True,
        "bmi": bmi,
        "category": category,
        "color": color,
        "advice": advice,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
