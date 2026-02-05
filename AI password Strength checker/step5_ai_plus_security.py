import pandas as pd
import math
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load trained data
data = pd.read_csv("password_features.csv")

X = data.drop("strength", axis=1)
y = data["strength"]

# Create pipeline (scaling + model)
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

# Train model
pipeline.fit(X, y)

# Entropy calculation
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

# Feature extraction
def extract_features(password):
    length = len(password)
    digit_count = sum(c.isdigit() for c in password)
    upper_count = sum(c.isupper() for c in password)
    lower_count = sum(c.islower() for c in password)
    special_count = sum(not c.isalnum() for c in password)
    entropy = calculate_entropy(password)

    return [length, digit_count, upper_count, lower_count, special_count, entropy]

# Cybersecurity rules
def apply_security_rules(password, ai_prediction, entropy):
    common_words = ["password", "admin", "welcome", "user", "login"]

    # Rule 1: very short password
    if len(password) < 8:
        return 0

    # Rule 2: common word present
    for word in common_words:
        if word in password.lower():
            return 0

    # Rule 3: strong entropy upgrade (safe)
    if entropy >= 60 and len(password) >= 14:
        return 2

    # Rule 4: no special characters → downgrade
    if not any(not c.isalnum() for c in password):
        return max(ai_prediction - 1, 0)

    return ai_prediction

# User input
password = input("Enter a password: ")

features = extract_features(password)
entropy = calculate_entropy(password)

ai_prediction = pipeline.predict([features])[0]
final_prediction = apply_security_rules(password, ai_prediction, entropy)

# Output
if final_prediction == 0:
    print("Final Strength: WEAK")
elif final_prediction == 1:
    print("Final Strength: MEDIUM")
else:
    print("Final Strength: STRONG")
