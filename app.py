import os
import csv
from flask import Flask, render_template, request
from models import db, Question

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()
    # Import data from CSV file
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            question = Question(question=row[0], answer=row[1])
            db.session.add(question)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        answer = Question.query.filter_by(question=question).first()
        if answer:
            return answer.answer
        else:
            return "Sorry, I couldn't find an answer for that question."

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)