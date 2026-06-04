import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

print("Step 1: Loading dataset...")
df = pd.read_csv("dataset.csv")

# Clean the data (remove rows where salary or description is missing)
df = df.dropna(subset=['salary_avg', 'description'])
df['work_from_home'] = df['work_from_home'].fillna(False).astype(int)

print("Step 2: Extracting feature matrix (This might take a few seconds)...")
# These are the core variables the AI will learn to evaluate
core_skills = [
    'python', 'sql', 'aws', 'azure', 'gcp', 'java', 'c++', 
    'react', 'node', 'tableau', 'excel', 'machine learning', 
    'spark', 'hadoop', 'api', 'docker'
]

# Create binary columns for the AI (1 if skill exists in job, 0 if not)
# FIX APPLIED: Added regex=False to prevent the 'c++' symbol crash
for skill in core_skills:
    df[skill] = df['description'].str.lower().str.contains(skill, regex=False).astype(int)

# Prepare Features (X) and Target (y)
X = df[core_skills + ['work_from_home']]
y = df['salary_avg']

# Split data into 80% Training and 20% Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Step 3: Training the Random Forest AI Model...")
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Test the AI's accuracy
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"--> AI Verification Complete. Model Error Margin: ±${mae:,.0f}")

print("Step 4: Exporting the AI Brain to disk...")
joblib.dump(model, "salary_model.pkl")
joblib.dump(core_skills, "model_features.pkl")
print("✅ Success! 'salary_model.pkl' has been generated.")