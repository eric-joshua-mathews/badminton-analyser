from flask import Flask, render_template, request, redirect, url_for, jsonify, json
#from flask_sqlalchemy import SQLAlchemy
from utils.guess_shot import guess_shot
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


@app.route('/save_shot', methods=['POST'])
def save_shot():
    pass


@app.route('/end_rally', methods=['POST'])
def end_rally():
    pass


@app.route('/guess_shot', methods=['POST'])
def _route():
  data = request.get_json()
  playerLocation=data["playerLocation"]
  shuttleLocation=data["shuttleLocation"]
  Px = data["Px"]
  Sx = data["Sx"]
  result = guess_shot(shuttleLocation,playerLocation,Px,Sx)
  return jsonify({"shot":result})


if __name__ == '__main__':
    app.run(debug=True)