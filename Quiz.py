
from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = 'kRxSUCjUBwNcVgPA3w1U'

def fetch_questions():
    with open('questions.json', encoding='utf-8') as file:
        return json.load(file)['questions']
    


@app.route('/')
def index():
    questions = fetch_questions()
    session['questions'] = random.sample(questions, len(questions))
    session['question_num'] = 0
    session['score'] = 0
    return redirect(url_for('quiz'))


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'questions' not in session or not session['questions']:
        return redirect(url_for('index'))

    questions = session.get('questions')
    question_num = session.get('question_num', 0)
    score = session.get('score', 0)

    if question_num >= len(questions):
        return redirect(url_for('result', score=score))


    if request.method == 'POST':
        user_answer = request.form['answer']
        correct_answer = questions[question_num]['answer']

        if user_answer == correct_answer:
            score += 10
            session['score'] = score

        session['question_num'] = question_num + 1
        return redirect(url_for('quiz'))
    
    question = questions[question_num]
    return render_template('quiz.html', question=question, question_num=question_num, score=score)


@app.route('/result/<int:score>')
def result(score):
    return render_template('result.html', score=score)


if __name__ == '__main__':
    app.run(debug=True)
