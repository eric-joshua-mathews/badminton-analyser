from flask import Flask, render_template, request, redirect, url_for, jsonify, json
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
DATA_FILE = 'data/shots.json'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/videoless')
def videoless_input():
    return render_template('videoless.html')


@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    pass


@app.route('/results')
def results():
    return render_template('results.html')


@app.route('/save_shot', methods=['POST'])
def save_shot():
    pass


@app.route('/end_rally', methods=['POST'])
def end_rally():
    pass


@app.route('/guess_shot', methods=['POST'])
def guess_shot():
  pass

if __name__ == '__main__':
    app.run(debug=True)