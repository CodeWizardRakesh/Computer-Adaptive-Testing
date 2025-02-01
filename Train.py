from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import joblib

# Load data
df = pd.read_csv("Dataset/adaptive_test_dataset.csv")

# Encode categorical features
le_diff = LabelEncoder()
le_topic = LabelEncoder()

df["current_difficulty"] = le_diff.fit_transform(df["current_difficulty"])
df["topic"] = le_topic.fit_transform(df["topic"])
df["next_difficulty"] = le_diff.transform(df["next_difficulty"])

# Features and target
X = df[["topic", "current_difficulty", "avg_time_spent", "avg_attempts", "success_rate"]]
y = df["next_difficulty"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred, target_names=le_diff.classes_))

# Save artifacts
joblib.dump(model, "Dataset/difficulty_predictor.pkl")
joblib.dump(scaler, "Dataset/scaler.pkl")
joblib.dump(le_diff, "Dataset/label_encoder.pkl")
