import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Define and fit the model and encoders
model = RandomForestClassifier(n_estimators=100, random_state=42)
scaler = StandardScaler()
le_diff = LabelEncoder()
le_topic = LabelEncoder()

# Example data (replace with your actual data)
X = [[1, 2], [3, 4], [5, 6]]
y_diff = ['easy', 'medium', 'hard']
y_topic = ['math', 'science', 'history']

# Fit the scaler and encoders
scaler.fit(X)
le_diff.fit(y_diff)
le_topic.fit(y_topic)

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
    current_diff='easy', 
    avg_time=45, 
    avg_attempts=3, 
    success_rate=0.8
))  # Output: The predicted difficulty level
