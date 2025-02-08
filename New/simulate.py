import pandas as pd
import joblib  # To load the trained model
import os
import time

# Load the trained model
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "../Model/suggest_diff.pkl")
model = joblib.load(model_path)  # Make sure your trained model is saved as suggest_diff.pkl

# Simulating the test where the user provides input
user_id = "U1"
topic = "T1"
correct = int(input("Did you answer correctly? (1 for Yes, 0 for No): "))  # User chooses correct or wrong

print("Start answering the question...")
start_time = time.time()  # Record start time
input("Press Enter when you finish answering...")
end_time = time.time()  # Record end time

time_spent = int(end_time - start_time)  # Calculate time spent
attempts = int(input("Enter number of attempts made: "))  # User inputs attempts

difficulty_test1 = "Medium"  # Predefined difficulty

test_data = pd.DataFrame({
    "User_ID": [user_id],
    "Topic": [topic],
    "Correct": [correct],
    "Time_Spent": [time_spent],
    "Attempts": [attempts],
    "Difficulty_Test1": [difficulty_test1]
})

# Convert categorical difficulty to numerical values
difficulty_mapping = {"Easy": 0, "Medium": 1, "Hard": 2}
test_data["Difficulty_Test1"] = test_data["Difficulty_Test1"].map(difficulty_mapping)

# Selecting features for prediction
features = test_data[["Correct", "Time_Spent", "Attempts", "Difficulty_Test1"]]

# Predict the difficulty level for the next test
predicted_difficulty = model.predict(features)

# Convert numerical predictions back to labels
inverse_difficulty_mapping = {0: "Easy", 1: "Medium", 2: "Hard"}
test_data["Suggested_Difficulty_Test2"] = predicted_difficulty[0]
test_data["Suggested_Difficulty_Test2"] = test_data["Suggested_Difficulty_Test2"].map(inverse_difficulty_mapping)

# Save the test performance data to CSV
test_data.to_csv("test2_performance.csv", index=False)

print("Test simulation complete. Results saved to test2_performance.csv")
