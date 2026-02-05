import pandas as pd
import math
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load training data
data = pd.read_csv("password_features.csv")

X = data.drop("strength", axis=1)
y = data["strength"]

# Create pipeline (same as training)
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

# Train the model
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

# Feature extraction function
def extract_features(password):
    length = len(password)
    digit_count = sum(c.isdigit() for c in password)
    upper_count = sum(c.isupper() for c in password)
    lower_count = sum(c.islower() for c in password)
    special_count = sum(not c.isalnum() for c in password)
    entropy = calculate_entropy(password)

    return [[length, digit_count, upper_count, lower_count, special_count, entropy]]

# Take user input
user_password = input("Enter a password: ")

# Extract features
features = extract_features(user_password)

# Predict strength
prediction = pipeline.predict(features)[0]

# Convert number to label
if prediction == 0:
    print("Password Strength: WEAK")
elif prediction == 1:
    print("Password Strength: MEDIUM")
else:
    print("Password Strength: STRONG")
