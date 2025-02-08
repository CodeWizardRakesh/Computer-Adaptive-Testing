import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Example data for fitting (replace with your actual data)
X_fit = np.array([
    [1, 1, 10, 2, 0.9],
    [2, 2, 20, 3, 0.8],
    [3, 3, 30, 4, 0.7],
    [4, 1, 40, 5, 0.6]
])
y_diff = ['easy', 'medium', 'hard', 'easy']
y_topic = ['math', 'science', 'history', 'math']

# Define and fit the model and encoders
model = RandomForestClassifier(n_estimators=100, random_state=42)
scaler = StandardScaler()
le_diff = LabelEncoder()
le_topic = LabelEncoder()

# Fit the scaler and encoders with the example data
scaler.fit(X_fit)
le_diff.fit(y_diff)
le_topic.fit(y_topic)

# Fit the model
model.fit(X_fit, le_diff.transform(y_diff))

# Save artifacts
joblib.dump(model, "Model/difficulty_predictor.pkl")
joblib.dump(scaler, "Model/scaler.pkl")
joblib.dump(le_diff, "Model/label_encoder_diff.pkl")
joblib.dump(le_topic, "Model/label_encoder_topic.pkl")

# Load artifacts
model = joblib.load("Model/difficulty_predictor.pkl")
scaler = joblib.load("Model/scaler.pkl")
le_diff = joblib.load("Model/label_encoder_diff.pkl")
le_topic = joblib.load("Model/label_encoder_topic.pkl")

def suggest_difficulty(topic, current_diff, avg_time, avg_attempts, success_rate):
    # Encode inputs
    topic_encoded = le_topic.transform([topic])[0]
    current_diff_encoded = le_diff.transform([current_diff])[0]
    
    # Prepare features
    features = np.array([[topic_encoded, current_diff_encoded, avg_time, avg_attempts, success_rate]])
    features_scaled = scaler.transform(features)
    
    # Predict
    pred = model.predict(features_scaled)
    return le_diff.inverse_transform(pred)[0]

# Example usage
print(suggest_difficulty(
    topic='math', 
    current_diff='hard', 
    avg_time=45, 
    avg_attempts=3, 
    success_rate=0.8
))  # Output: The predicted difficulty level
