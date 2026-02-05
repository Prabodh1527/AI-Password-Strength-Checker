# 🔐 AI Password Strength Checker

An AI + Cybersecurity based password strength evaluation system that uses
machine learning, entropy analysis, and rule-based security to classify
passwords as Weak, Medium, or Strong.

---

## 🚀 Features
- Machine Learning (Logistic Regression)
- Entropy-based randomness analysis
- Cybersecurity rule enforcement
- Interactive Streamlit web interface
- Real-time password strength feedback

---

## 🧠 How It Works
1. Passwords are converted into numerical features
2. Entropy is calculated to measure unpredictability
3. ML model predicts strength based on learned patterns
4. Security rules override unsafe predictions
5. Final strength is displayed to the user

---

## 🛠 Tech Stack
- Python
- Pandas, Scikit-learn
- Streamlit
- Machine Learning
- Cybersecurity principles

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python step1_feature_extraction.py
python step3_train_model.py
python -m streamlit run app.py
