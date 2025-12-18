from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib

# -------------------------
# Load trained artifacts
# -------------------------
scaler = joblib.load("models/scaler.pkl")
model = joblib.load("models/logistic_model.pkl")

feature_names = scaler.feature_names_in_

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(
    title="Fraud Detection API",
    description="Real-time credit card fraud risk scoring system",
    version="1.0"
)

# -------------------------
# Root Endpoint
# -------------------------
@app.get("/")
def home():
    return {"message": "Fraud Detection API is running"}

# ======================================================
# ADD 6 — Accept Transaction Inputs (Pydantic Model)
# ======================================================
class Transaction(BaseModel):
    amount: float
    country: str
    channel: str
    international: bool
    card_type: str

# ======================================================
# Prediction Endpoint
# ======================================================
@app.post("/predict")
def predict(transaction: dict):
    """
    transaction contains:
    - Amount, Time, V1–V28 (used by model)
    - Extra fields like country, channel, etc. (ignored by model)
    """

    # -------------------------
    # Convert input to DataFrame
    # -------------------------
    df = pd.DataFrame([transaction])

    # Keep only model-required features
    df = df[feature_names]

    # -------------------------
    # Scale features
    # -------------------------
    scaled = scaler.transform(df)

    # -------------------------
    # Predict probability
    # -------------------------
    fraud_probability = model.predict_proba(scaled)[0][1]
    risk_score = round(fraud_probability * 100)

    # -------------------------
    # Decision Logic (Bank-style)
    # -------------------------
    if risk_score < 30:
        decision = "APPROVE"
    elif risk_score < 70:
        decision = "VERIFY"
    else:
        decision = "BLOCK"

    # ======================================================
    # ADD 7 — Return Decision Logic
    # ======================================================
    return {
        "fraud_probability": float(fraud_probability),
        "risk_score": risk_score,
        "decision": decision
    }
