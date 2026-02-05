import pandas as pd

# Load the dataset
data = pd.read_csv("passwords.csv")

# Show first 5 rows
print("First 5 rows of the dataset:")
print(data.head())

# Show total number of rows
print("\nTotal rows in dataset:", len(data))
