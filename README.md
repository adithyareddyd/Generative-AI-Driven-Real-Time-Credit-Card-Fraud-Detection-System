\# Generative AI–Driven Real-Time Credit Card Fraud Detection System



An end-to-end, industry-style \*\*real-time credit card fraud detection system\*\* that scores live credit card transactions, computes risk, and triggers OTP-based customer verification for suspicious activity. The system uses supervised machine learning and a real-time decision engine with a Streamlit monitoring dashboard.



This project is designed to mimic how \*\*modern banks and fintech companies\*\* build fraud detection pipelines using anonymized/synthetic transaction data.



---



\## 🔍 Project Overview



Credit card fraud detection is challenging due to:



\- Extreme class imbalance in transactions (very few frauds).

\- Constantly evolving fraud patterns.

\- Need for low-latency, real-time decisions.

\- Regulatory and explainability requirements.



This system processes each transaction event in real time:



Transaction Event → Model Inference → Risk Score (0–100) →  

Decision Engine (APPROVE / VERIFY / BLOCK) → OTP Flow (if needed) → Dashboard \& Monitoring



---



\## 🧠 System Architecture (High-Level)



Simulated / User-Entered Transaction  

↓  

Data Preprocessing \& Feature Construction  

↓  

Supervised Fraud Model (Logistic Regression / XGBoost)  

↓  

Risk Scoring Engine (0–100)  

↓  

Decision Engine (APPROVE / VERIFY / BLOCK)  

↓  

OTP-Based Verification for high-risk cases (simulated)  

↓  

Real-Time Streamlit Dashboard + KPIs \& Trends



> Optional / planned extensions: Autoencoder-based anomaly detection, VAE-based generative modeling, and SHAP explainability notebooks.



---



\## 📌 Project Phases



\### 🔹 Phase 1: Supervised Fraud Detection



\- Train baseline fraud models using anonymized credit card transaction data.  

\- Algorithms: Logistic Regression and tree-based models (e.g., XGBoost).  

\- Focus on \*\*recall for fraud class\*\* and \*\*Precision–Recall AUC\*\*, instead of accuracy only, due to class imbalance.



\### 🔹 Phase 2: Risk Scoring \& Decision Engine



\- Convert model fraud probability into a \*\*0–100 risk score\*\*.  

\- Bank-style thresholds (configurable):



&nbsp; - 0–30 → \*\*APPROVE\*\*  

&nbsp; - 31–70 → \*\*VERIFY (OTP)\*\*  

&nbsp; - 71–100 → \*\*BLOCK\*\*



\### 🔹 Phase 3: Real-Time API (FastAPI)



\- Expose the trained model via a FastAPI `/predict` endpoint.  

\- Accepts JSON transaction payload and returns:



&nbsp; - `fraud\_probability`  

&nbsp; - `risk\_score`  

&nbsp; - `decision` (APPROVE / VERIFY / BLOCK)



\### 🔹 Phase 4: Real-Time Dashboard (Streamlit)



\- Transaction input panel (amount, country, channel, international flag, card type).  

\- Transaction details + fraud probability + risk level + decision.  

\- OTP verification flow for VERIFY/BLOCK transactions (demo OTP shown on screen).  

\- Recent transactions table with status, risk, and decision.  

\- Monitoring KPIs: total, approved, review, blocked, estimated fraud prevented.  

\- Simple risk trend chart (Low / Medium / High risk counts).



\### 🔹 Phase 5 (Optional, if implemented): Advanced Modeling



\- \*\*Unsupervised anomaly detection\*\* (Autoencoder).  

\- \*\*Generative modeling\*\* (VAE) for synthetic fraud patterns.  

\- \*\*Explainability\*\* with SHAP for audit/regulatory reports.



Mark these as implemented or planned depending on your current notebooks.



---



\## ⚙️ Tech Stack



\- \*\*Language:\*\* Python  

\- \*\*ML:\*\* scikit-learn, XGBoost (optionally TensorFlow / Keras for Autoencoder/VAE)  

\- \*\*API:\*\* FastAPI, Uvicorn  

\- \*\*Dashboard:\*\* Streamlit  

\- \*\*Data:\*\* pandas, NumPy (anonymized / synthetic credit card transaction CSV)  

\- \*\*Visualization:\*\* Matplotlib / Streamlit charts  



---



\## 📂 Repository Structure



Adapt to your actual layout; for example:



Generative-AI-Driven-Real-Time-Credit-Card-Fraud-Detection-System/

│

├── notebooks/ # Modeling \& experiments

│ ├── 01\_Baseline\_Fraud\_Detection.ipynb

│ ├── 02\_Risk\_Scoring.ipynb

│ ├── 03\_Autoencoder\_Anomaly\_Detection.ipynb # (optional)

│ ├── 04\_VAE\_Generative\_Modeling.ipynb # (optional)

│ └── 05\_SHAP\_Explainability.ipynb # (optional)

│

├── src/

│ ├── api.py # FastAPI service

│ └── dashboard.py # Streamlit real-time dashboard

│

├── models/ # Saved model artifacts

├── data/ # Dataset (kept local / ignored in Git)

├── requirements.txt

└── README.md



If your filenames differ, update `api.py` / `dashboard.py` accordingly.



---



\## ▶️ How to Run the Project



\### 1️⃣ Install dependencies



pip install -r requirements.txt





\### 2️⃣ Start the FastAPI backend

uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload





(or `uvicorn api:app --reload` if `api.py` is in the root).



\### 3️⃣ Start the Streamlit dashboard

streamlit run src/dashboard.py





(or `streamlit run dashboard.py` if it is in the root).



Open `http://localhost:8501` in your browser.



---



\## 🛡️ Data \& Privacy



\- Uses \*\*anonymized / synthetic credit card transaction data\*\*; no real card numbers, CVV, PIN, or personally identifiable information are used. \[web:71]\[web:106]\[web:95]  

\- OTP verification is \*\*simulated\*\* for demonstration and is not connected to any real mobile or email service.



---



\## ⚠️ Disclaimer



This project is for educational and demonstration purposes only.  

It is \*\*not\*\* intended for production use or for processing real payment card data without full security, PCI‑DSS compliance, and regulatory approvals. \[web:89]\[web:92]





