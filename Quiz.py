
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_questions():
    with open('questions.json', 'r') as file:
        return json.load(file)['questions']
    


@app.route('/')
def index():
    return redirect(url_for('quiz', question_num=0, score=0))

@app.route('/quiz/<int:question_num>/<int:score>', methods=['GET', 'POST'])
def quiz(question_num, score):
    questions = load_questions()


    if request.method == 'POST':
        user_answer = request.form['answer']
        correct_answer = questions[question_num]['answer']

        if user_answer == correct_answer:
            score += 10

        question_num += 1

        if question_num >= len(questions):
            return redirect(url_for('result', score=score))
    
    question = questions[question_num]
    return render_template('quiz.html', question=question, question_num=question_num, score=score)


@app.route('/result/<int:score>')
def result(score):
    return render_template('result.html', score=score)


if __name__ == '__main__':
    app.run(debug=True)
