import streamlit as st
import requests
import random

# -------------------------
# Session State
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "otp" not in st.session_state:
    st.session_state.otp = None

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    layout="centered"
)

# -------------------------
# Title
# -------------------------
st.title("💳 Real-Time Fraud Detection Dashboard")
st.write("Simulated transaction risk scoring (Bank-style)")

# -------------------------
# Sidebar: Transaction Input
# -------------------------
st.sidebar.header("💳 Transaction Input")

amount = st.sidebar.number_input(
    "Transaction Amount (₹)",
    min_value=1.0,
    step=100.0,
    format="%.2f"
)

country = st.sidebar.selectbox("Country", ["India", "USA", "UK", "Germany"])
channel = st.sidebar.radio("Channel", ["Online", "Swipe"])
international = st.sidebar.checkbox("International")
card_type = st.sidebar.selectbox("Card Type", ["Debit", "Credit"])

predict_btn = st.sidebar.button("Submit Transaction")

# -------------------------
# Transaction Details
# -------------------------
st.subheader("Transaction Details")
st.write(f"Amount: ₹{amount:,.2f}")
st.write(f"Country: {country}")
st.write(f"Channel: {channel}")
st.write(f"International: {international}")
st.write(f"Card Type: {card_type}")

# -------------------------
# API URL
# -------------------------
API_URL = "http://127.0.0.1:8000/predict"

# -------------------------
# Risk Label
# -------------------------
def risk_label(score):
    if score < 30:
        return "🟢 LOW"
    elif score < 70:
        return "🟡 MEDIUM"
    else:
        return "🔴 HIGH"

# -------------------------
# Create transaction payload
# -------------------------
def create_transaction():
    data = {
        "Time": random.uniform(0, 100000),
        "Amount": float(amount),
    }
    data.update({f"V{i}": random.uniform(-2, 2) for i in range(1, 29)})
    return data

# -------------------------
# Prediction Logic
# -------------------------
if predict_btn:
    transaction = create_transaction()

    try:
        response = requests.post(API_URL, json=transaction)

        if response.status_code == 200:
            result = response.json()

            fraud_prob = result["fraud_probability"]
            risk_score = result["risk_score"]
            decision = result["decision"]

            st.subheader("🔍 Transaction Result")
            st.metric("Fraud Probability", round(fraud_prob, 6))
            st.metric("Risk Score", risk_score)

            # -------------------------
            # Risk Analysis
            # -------------------------
            st.subheader("🧠 Risk Analysis")
            risk_text = risk_label(risk_score)

            st.markdown(f"""
**Fraud Probability:** {fraud_prob:.4f} ({fraud_prob*100:.2f}%)  
**Risk Level:** {risk_text}  
**Bank Decision:** **{decision}**
""")

            # -------------------------
            # OTP Verification
            # -------------------------
            st.subheader("🔐 Bank Verification Request")
            st.caption(
                "In a real system, an OTP would be sent to the customer’s "
                "registered mobile/email. This panel simulates that process."
            )

            if "VERIFY" in decision or "BLOCK" in decision:

                if st.session_state.otp is None and not st.session_state.otp_verified:
                    st.session_state.otp = random.randint(100000, 999999)

                    st.warning(
                        "⚠️ Suspicious transaction detected.\n\n"
                        f"Transaction Amount: ₹{amount:,.0f}\n"
                        f"Location: {country}\n\n"
                        "An OTP has been sent to your registered mobile/email."
                    )

                    # Demo only
                    st.caption(f"Demo OTP (for project): {st.session_state.otp}")

                if not st.session_state.otp_verified:
                    entered_otp = st.text_input("Enter OTP", max_chars=6)

                    if st.button("Verify OTP"):
                        if entered_otp == str(st.session_state.otp):
                            st.success("OTP verified successfully. Transaction approved.")
                            st.session_state.otp_verified = True
                            st.session_state.otp = None
                        else:
                            st.error("Invalid OTP. Transaction blocked for security reasons.")
                else:
                    st.success("Transaction already verified successfully.")

            else:
                st.success("Transaction approved. No verification required.")

            # -------------------------
            # Update Decision After OTP
            # -------------------------
            final_decision = decision
            if st.session_state.otp_verified and ("VERIFY" in decision or "BLOCK" in decision):
                final_decision = "APPROVED_AFTER_OTP"

            # -------------------------
            # Store Transaction
            # -------------------------
            status_icon = "🟢" if risk_score < 30 else "🟡" if risk_score < 70 else "🔴"

            st.session_state.history.append({
                "Status": status_icon,
                "Amount": float(amount),
                "Country": country,
                "Probability": round(fraud_prob, 4),
                "Risk": risk_text,
                "Decision": final_decision
            })

            # Reset OTP verified flag for next transaction
            st.session_state.otp_verified = False

        else:
            st.error("API not reachable. Make sure FastAPI is running.")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")

# -------------------------
# Recent Transactions
# -------------------------
st.subheader("Recent Transactions")
st.table(st.session_state.history[-10:])

# -------------------------
# Monitoring & Alerts
# -------------------------
st.subheader("📈 Monitoring & Alerts")

total_tx = len(st.session_state.history)
blocked = sum(1 for h in st.session_state.history if "BLOCK" in h["Decision"])
review = sum(1 for h in st.session_state.history if "VERIFY" in h["Decision"])
approved = total_tx - blocked - review

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Tx", total_tx)
c2.metric("Approved", approved)
c3.metric("Review", review)
c4.metric("Blocked", blocked)

fraud_prevented = sum(
    h["Amount"] for h in st.session_state.history if "BLOCK" in h["Decision"]
)
st.metric("Estimated Fraud Prevented (₹)", fraud_prevented)

# -------------------------
# Fraud Alerts Trend (Simulated)
# -------------------------
st.subheader("📊 Fraud Alerts Trend (Simulated)")

risk_counts = {
    "Low Risk": sum(1 for h in st.session_state.history if h["Risk"] == "🟢 LOW"),
    "Medium Risk": sum(1 for h in st.session_state.history if h["Risk"] == "🟡 MEDIUM"),
    "High Risk": sum(1 for h in st.session_state.history if h["Risk"] == "🔴 HIGH"),
}

if sum(risk_counts.values()) == 0:
    st.info("No transactions yet to display trends.")
else:
    st.bar_chart(risk_counts)

# -------------------------
# Bottom Notes
# -------------------------
st.caption(
    "For suspicious transactions, the bank requests OTP verification "
    "before approval. This mirrors real-world fraud prevention systems."
)

st.caption(
    "⚠️ All data shown is simulated for demo purposes. No real card data is used."
)
