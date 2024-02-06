import mysql.connector
import time
import threading
from random import shuffle

db_connection = mysql.connector.connect(
    host="localhost",
    user=" root",
    password="kaif1234",
    database="quiz",
)

cursor = db_connection.cursor()

# answers=cursor.execute("Select * from answers")
# answers = cursor.fetchall()  # Fetch the results
# questions = cursor.execute("Select * from Questions")
# questions= cursor.fetchall()

questions_time_limit = 15

# print(questions)
# print(answers)

def get_quiz_questions(cursor):
    query = """
        SELECT questions.id, questions.question_text, answers.id, answers.answer_text, answers.correct_answer
        FROM questions
        JOIN answers ON questions.id = answers.question_id;
    """
    cursor.execute(query)
    questions = {}
    for row in cursor.fetchall():
        question_id, question_text, answer_id, answer_text, correct_answer = row
        if question_id not in questions:
            questions[question_id] = {"question_text": question_text, "answers": []}
        questions[question_id]["answers"].append({"answer_id": answer_id, "answer_text": answer_text, "is_correct": correct_answer})
        
        question_list = list(questions.values())
       
    return questions


def display_question(question, answers):
    start_time = time.time()
    print(question)
    for answer in answers:
        print(f"{answer['answer_id']}. {answer['answer_text']}")
    
    while True:
        user_answer = input("Enter the number of your answer: ")
        end_time = time.time()
        time_taken = end_time - start_time
        
        if time_taken > questions_time_limit:
            print("Time's up! Moving to the next question.")
            return None  # Return None to indicate no answer
        if user_answer.isnumeric() and 1 <= int(user_answer) <= len(answers):
            return int(user_answer)
        else:
            print("Invalid input. Please enter a valid answer number.")


def calculate_score(user_responses, questions):
    score = 0
    for question_id, user_answer in user_responses.items():
        correct_answer = next(answer for answer in questions[question_id]["answers"] if answer["is_correct"])
        if user_answer == correct_answer["answer_id"]:
            score += 1
    return score

def main():
    try:
        questions = get_quiz_questions(cursor)
        user_responses = {}
        for question_id, question_data in questions.items():
            user_answer = display_question(question_data["question_text"], question_data["answers"])
            if user_answer is None:
                # Handle the case when time's up
                print("Question not answered within the time limit. Moving to the next question.")
            else:
                user_responses[question_id] = int(user_answer)
        score = calculate_score(user_responses, questions)
        print(f"Your score is {score}/{len(questions)}")
    finally:
        cursor.close()
        db_connection.close()



if __name__ == "__main__":
    main()
