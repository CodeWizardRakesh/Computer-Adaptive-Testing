import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pandas as pd
import os
import joblib

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "../Dataset/user_performance.csv")

df = pd.read_csv(csv_path)
# print(df)
difficulty_mapping = {'Easy': 0, 'Medium': 1, 'Hard': 2}
df['Difficulty_Test1'] = df['Difficulty_Test1'].map(difficulty_mapping)
df['Suggested_Difficulty_Test2'] = df['Suggested_Difficulty_Test2'].map(difficulty_mapping)

# Features and target
X = df[['Correct', 'Time_Spent', 'Attempts', 'Difficulty_Test1']]
y = df['Suggested_Difficulty_Test2']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

model_dir = csv_path = os.path.join(script_dir, "../Model/suggest_diff.pkl")
joblib.dump(model, model_dir)