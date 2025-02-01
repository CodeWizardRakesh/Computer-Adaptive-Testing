import pandas as pd
import numpy as np

# Generate synthetic data
np.random.seed(42)
n_users = 500  # Number of users
topics = [1, 2, 3, 4, 5]
difficulties = ["Easy", "Medium", "Hard"]

data = []
for user in range(n_users):
    for topic in topics:
        # Randomly assign current difficulty
        current_diff = np.random.choice(difficulties, p=[0.3, 0.4, 0.3])
        
        # Simulate performance metrics
        avg_time = np.random.normal(loc=30 if current_diff == "Easy" else 45 if current_diff == "Medium" else 60, scale=10)
        avg_attempts = np.random.randint(1, 4) if current_diff == "Easy" else np.random.randint(2, 5)
        success_rate = np.clip(np.random.normal(loc=0.7 if current_diff == "Easy" else 0.5 if current_diff == "Medium" else 0.3, scale=0.15), 0, 1)
        
        # Define next difficulty based on rules (simulate ground truth)
        if success_rate > 0.75:
            next_diff = "Hard" if current_diff == "Medium" else "Medium" if current_diff == "Easy" else "Hard"
        elif success_rate < 0.4:
            next_diff = "Easy" if current_diff == "Medium" else "Medium" if current_diff == "Hard" else "Easy"
        else:
            next_diff = current_diff
        
        data.append([
            user, topic, current_diff, 
            np.abs(avg_time), avg_attempts, success_rate, next_diff
        ])

df = pd.DataFrame(data, columns=["user_id", "topic", "current_difficulty", 
                                  "avg_time_spent", "avg_attempts", "success_rate", 
                                  "next_difficulty"])
df.to_csv("Dataset/adaptive_test_dataset.csv", index=False)