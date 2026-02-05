import streamlit as st
import pandas as pd
import math
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Password Strength Checker",
    page_icon="🔐",
    layout="centered"
)

# -----------------------------
# CUSTOM STYLING (Minimal CSS)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: #00f5d4;
}
.password-box {
    background-color: #161b22;
    padding: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA + MODEL
# -----------------------------
data = pd.read_csv("password_features.csv")
X = data.drop("strength", axis=1)
y = data["strength"]

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

pipeline.fit(X, y)

# -----------------------------
# ENTROPY
# -----------------------------
def calculate_entropy(password):
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(not c.isalnum() for c in password):
        charset += 32
    return len(password) * math.log2(charset) if charset else 0

# -----------------------------
# FEATURE EXTRACTION
# -----------------------------
def extract_features(password):
    return [[
        len(password),
        sum(c.isdigit() for c in password),
        sum(c.isupper() for c in password),
        sum(c.islower() for c in password),
        sum(not c.isalnum() for c in password),
        calculate_entropy(password)
    ]]

# -----------------------------
# SECURITY RULES
# -----------------------------
def apply_security_rules(password, ai_prediction, entropy):
    common_words = ["password", "admin", "welcome", "user", "login"]

    if len(password) < 8:
        return 0

    for word in common_words:
        if word in password.lower():
            return 0

    if entropy >= 60 and len(password) >= 14:
        return 2

    if not any(not c.isalnum() for c in password):
        return max(ai_prediction - 1, 0)

    return ai_prediction

# -----------------------------
# UI START
# -----------------------------
st.markdown("<h1 style='text-align:center;'>🔐 AI Password Strength Checker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#9da5b4;'>AI + Cybersecurity powered password analysis</p>", unsafe_allow_html=True)



password = st.text_input("Enter your password", type="password")



if password:
    features = extract_features(password)
    entropy = calculate_entropy(password)

    ai_pred = pipeline.predict(features)[0]
    final_pred = apply_security_rules(password, ai_pred, entropy)

    # Strength meter
    strength_value = min(entropy / 80, 1.0)
    st.progress(strength_value)

    st.markdown(f"**Entropy Score:** `{round(entropy, 2)}`")

    if final_pred == 0:
        st.error("❌ WEAK PASSWORD")
        st.markdown("- Too easy to guess\n- Vulnerable to attacks")
    elif final_pred == 1:
        st.warning("⚠️ MEDIUM STRENGTH")
        st.markdown("- Better, but can be improved\n- Add more randomness")
    else:
        st.success("✅ STRONG PASSWORD")
        st.markdown("- Highly secure\n- Resistant to brute-force attacks")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<hr>
<p style='text-align:center; color:#6e7681;'>
Built using AI + Cybersecurity principles<br>
Entropy-based analysis • Machine Learning • Rule-based security
</p>
""", unsafe_allow_html=True)
