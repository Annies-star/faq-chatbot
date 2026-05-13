from flask import Flask, render_template, request
import mysql.connector
from difflib import get_close_matches

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="95974",
    database="faqbot"
)

@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""

    if request.method == "POST":

        user_question = request.form["question"].lower()

        cursor = db.cursor()

        # Get all questions and answers
        cursor.execute("SELECT question, answer FROM faq")
        data = cursor.fetchall()

        questions = []
        answers = {}

        for q, a in data:
            q = q.lower()
            questions.append(q)
            answers[q] = a

        # NLP using difflib
        match = get_close_matches(user_question, questions, n=1, cutoff=0.5)

        if match:
            answer = answers[match[0]]
        else:
            answer = "No answer found"

    return render_template("index.html", answer=answer)

app.run(debug=True)