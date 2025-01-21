import random
from typing import List, Dict, Optional

class Question:
    def __init__(self, text: str, correct_answer: str, difficulty: int):
        self.text = text
        self.correct_answer = correct_answer
        self.difficulty = difficulty  # 1 (easiest) to 5 (hardest)

class QuestionBank:
    def __init__(self):
        # Sample questions with varying difficulty levels
        self.questions = {
            1: [  # Easy questions
                Question("What is 2 + 2?", "4", 1),
                Question("What color is the sky on a clear day?", "blue", 1),
                Question("How many days are in a week?", "7", 1),
            ],
            2: [  # Medium-easy questions
                Question("What is 8 × 7?", "56", 2),
                Question("What is the capital of France?", "paris", 2),
                Question("What planet is known as the Red Planet?", "mars", 2),
            ],
            3: [  # Medium questions
                Question("What is the square root of 144?", "12", 3),
                Question("Who wrote Romeo and Juliet?", "william shakespeare", 3),
                Question("What is the chemical symbol for gold?", "au", 3),
            ],
            4: [  # Medium-hard questions
                Question("What is the value of π to 2 decimal places?", "3.14", 4),
                Question("In which year did World War II end?", "1945", 4),
                Question("What is the atomic number of carbon?", "6", 4),
            ],
            5: [  # Hard questions
                Question("What is the fibonacci sequence up to 5 numbers?", "1,1,2,3,5", 5),
                Question("What is the speed of light in km/s?", "299792", 5),
                Question("What is the charge of an electron?", "-1.602176634×10−19", 5),
            ]
        }

class Candidate:
    def __init__(self, name: str):
        self.name = name
        self.performance_history: List[Dict] = []
        self.current_difficulty = 3  # Start with medium difficulty

    def update_difficulty(self, score: float):
        """Update difficulty based on previous performance"""
        if score >= 0.8:  # If score is 80% or higher
            self.current_difficulty = min(5, self.current_difficulty + 1)
        elif score <= 0.4:  # If score is 40% or lower
            self.current_difficulty = max(1, self.current_difficulty - 1)
        # If score is between 40% and 80%, keep current difficulty

class AdaptiveQuizSystem:
    def __init__(self):
        self.question_bank = QuestionBank()
        self.candidates: Dict[str, Candidate] = {}

    def register_candidate(self, name: str) -> Candidate:
        """Register a new candidate in the system"""
        candidate = Candidate(name)
        self.candidates[name] = candidate
        return candidate

    def generate_quiz(self, candidate_name: str, num_questions: int = 3) -> List[Question]:
        """Generate a quiz for a candidate based on their current difficulty level"""
        candidate = self.candidates.get(candidate_name)
        if not candidate:
            raise ValueError(f"Candidate {candidate_name} not found")

        difficulty = candidate.current_difficulty
        # Get questions from current difficulty and adjacent difficulties
        available_questions = []
        for d in range(max(1, difficulty - 1), min(5, difficulty + 2)):
            available_questions.extend(self.question_bank.questions[d])
        
        return random.sample(available_questions, min(num_questions, len(available_questions)))

    def evaluate_quiz(self, candidate_name: str, answers: List[str], questions: List[Question]) -> float:
        """Evaluate quiz performance and update candidate's difficulty level"""
        if len(answers) != len(questions):
            raise ValueError("Number of answers must match number of questions")

        candidate = self.candidates.get(candidate_name)
        if not candidate:
            raise ValueError(f"Candidate {candidate_name} not found")

        # Calculate score
        correct = sum(1 for ans, q in zip(answers, questions) 
                     if ans.lower().strip() == q.correct_answer.lower().strip())
        score = correct / len(questions)

        # Record performance
        performance = {
            "difficulty": candidate.current_difficulty,
            "score": score,
            "num_questions": len(questions)
        }
        candidate.performance_history.append(performance)

        # Update difficulty for next quiz
        candidate.update_difficulty(score)

        return score

def main():
    # Example usage
    quiz_system = AdaptiveQuizSystem()
    
    # Register a new candidate
    candidate_name = "John Doe"
    quiz_system.register_candidate(candidate_name)
    
    # Run three quiz sessions
    for session in range(3):
        print(f"\nQuiz Session {session + 1}")
        print(f"Current difficulty level: {quiz_system.candidates[candidate_name].current_difficulty}")
        
        # Generate quiz
        questions = quiz_system.generate_quiz(candidate_name)
        
        # Simulate taking the quiz (in a real system, this would be user input)
        answers = []
        for i, question in enumerate(questions, 1):
            print(f"\nQuestion {i}: {question.text}")
            # In this example, we'll simulate correct answers for demonstration
            answers.append(question.correct_answer)
        
        # Evaluate quiz
        score = quiz_system.evaluate_quiz(candidate_name, answers, questions)
        print(f"\nScore: {score * 100:.1f}%")
        print(f"Next quiz difficulty level: {quiz_system.candidates[candidate_name].current_difficulty}")

if __name__ == "__main__":
    main()