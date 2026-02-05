import pandas as pd
import math

# Load the dataset
data = pd.read_csv("passwords.csv")

# Calculate entropy
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

    if charset == 0:
        return 0

    return len(password) * math.log2(charset)

# Extract features
def extract_features(password):
    length = len(password)
    digit_count = sum(c.isdigit() for c in password)
    upper_count = sum(c.isupper() for c in password)
    lower_count = sum(c.islower() for c in password)
    special_count = sum(not c.isalnum() for c in password)
    entropy = calculate_entropy(password)

    return [length, digit_count, upper_count, lower_count, special_count, entropy]

# Apply feature extraction
features = data["password"].apply(extract_features)

# Create DataFrame
feature_df = pd.DataFrame(
    features.tolist(),
    columns=["length", "digits", "upper", "lower", "special", "entropy"]
)

# Add strength column
final_df = pd.concat([feature_df, data["strength"]], axis=1)

# Save features
final_df.to_csv("password_features.csv", index=False)

print("Feature extraction completed successfully")
