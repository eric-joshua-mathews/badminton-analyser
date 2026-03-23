from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
#from flask_sqlalchemy import SQLAlchemy
from utils.guess_shot import guess_shot
from utils.generate_stats import generate_stats
import os
match_file="data/match_data.json"
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
    data = request.get_json()
    # load existing match data or create new
    if os.path.exists(match_file):
        with open(match_file, "r") as f:
            content = f.read().strip()
            match_data = json.loads(content) if content else {"rallies": []}
    else:
        match_data = {"rallies": []}
    # append rally
    match_data["rallies"].append(data)
    # save back to file
    with open(match_file, "w") as f:
        json.dump(match_data, f, indent=2)
    return jsonify({"status": "ok"})

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

@app.route('/stats')
def stats():
    stats = generate_stats()
    if not stats:
        return "No match data found", 404
    return render_template('stats.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True)