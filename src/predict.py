import pandas as pd
import numpy as np
import joblib

scaler = joblib.load("models/scaler.pkl")
model = joblib.load("models/logistic_model.pkl")

# Create feature names (same as training)
feature_names = scaler.feature_names_in_

# Create transaction as DataFrame
transaction = pd.DataFrame(
    np.random.rand(1, len(feature_names)),
    columns=feature_names
)

transaction_scaled = scaler.transform(transaction)
fraud_prob = model.predict_proba(transaction_scaled)[0][1]

risk_score = round(fraud_prob * 100)

if risk_score < 30:
    decision = "APPROVE"
elif risk_score < 70:
    decision = "VERIFY"
else:
    decision = "BLOCK"

print("Fraud probability:", fraud_prob)
print("Risk score:", risk_score)
print("Decision:", decision)
