from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib  # To load the trained model
import os
import time

app = Flask(__name__)

# Load the trained model
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "../Model/suggest_diff.pkl")
model = joblib.load(model_path)

difficulty_mapping = {"Easy": 0, "Medium": 1, "Hard": 2}
inverse_difficulty_mapping = {0: "Easy", 1: "Medium", 2: "Hard"}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    user_id = "U1"
    topic = "T1"
    correct = data["correct"]
    time_spent = data["time_spent"]
    attempts = data["attempts"]
    difficulty_test1 = "Medium"  # Predefined difficulty
    
    test_data = pd.DataFrame({
        "User_ID": [user_id],
        "Topic": [topic],
        "Correct": [correct],
        "Time_Spent": [time_spent],
        "Attempts": [attempts],
        "Difficulty_Test1": [difficulty_test1]
    })
    
    test_data["Difficulty_Test1"] = test_data["Difficulty_Test1"].map(difficulty_mapping)
    features = test_data[["Correct", "Time_Spent", "Attempts", "Difficulty_Test1"]]
    predicted_difficulty = model.predict(features)[0]
    test_data["Suggested_Difficulty_Test2"] = predicted_difficulty
    test_data["Suggested_Difficulty_Test2"] = test_data["Suggested_Difficulty_Test2"].map(inverse_difficulty_mapping)
    test_data.to_csv("test2_performance.csv", index=False, mode='a', header=not os.path.exists("test2_performance.csv"))
    
    return jsonify({"suggested_difficulty": inverse_difficulty_mapping[predicted_difficulty]})

if __name__ == '__main__':
    app.run(debug=True)
