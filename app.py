from flask import Flask, render_template, request, redirect, url_for, jsonify,session
import json
from utils.db_helpers import get_or_create_player, get_db_connection, insert_rally, create_match
#from flask_sqlalchemy import SQLAlchemy
from utils.guess_shot import guess_shot
from utils.generate_stats import generate_stats
from utils.feedback_api import get_ai_feedback
import os
match_file="data/match_data.json"
app = Flask(__name__)
app.secret_key="bananaAppleSauce"
DATA_FILE = 'data/shots.json'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/videoless',methods=['POST'])
def videoless_input():
    if request.method == 'POST':
        player1_name=request.form.get("player1","").strip()
        player2_name=request.form.get("player2","").strip()
        if not player1_name or not player2_name:
            return render_template("index.html",error="Please enter both player names")

        p1_id = get_or_create_player(player1_name)
        p2_id = get_or_create_player(player2_name)
        match_id = create_match(p1_id, p2_id)

        session["match_id"] = match_id
        session["player1_id"] = p1_id
        session["player2_id"] = p2_id
        conn = get_db_connection()
        cur=conn.cursor()
        cur.execute("""
        INSERT INTO Matches (PlayerOneID,PlayerTwoID,WinnerID) VALUES (?,?,NULL)
        """,(p1_id,p2_id,))
        conn.commit()
        match_id=cur.lastrowid
        conn.close()
        session['match_id'] = match_id
        session['player1_name'] = player1_name
        session['player2_name'] = player2_name
        session['player1_id'] = p1_id
        session['player2_id'] = p2_id
        return render_template('videoless.html',
                               player1_name=player1_name,
                               player2_name=player2_name)
        return redirect(url_for('index')) #for get req

@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    pass


@app.route('/save_shot', methods=['POST'])
def save_shot():
    #json
    print("session cont:", dict(session))
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
    #db save
    match_id=session.get('match_id')
    player1_id=session.get('player1_id')
    player2_id=session.get('player2_id')
    if not match_id or not player1_id or not player2_id:
        return jsonify({"error":"No active match in session"}),400
    try:
        insert_rally(match_id,data,player1_id,player2_id)
    except Exception as e:
        print(f"error inserting rally: {e}")
        return jsonify({"error":f"db insert failed: {e}"}),500
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
    stats_data = generate_stats()

    try:
        with open(match_file, "r") as f:
            match_data = json.load(f)
    except Exception as e:
        return f"unable to load match_data: {e}"
    if not stats_data:
        return "No match data found", 404

    try:
        ai_feedback_p1 = get_ai_feedback(match_data, 1)
    except Exception as e:
        ai_feedback_p1 = f"AI feedback unavailable for Player 1: {e}"

    try:
        ai_feedback_p2 = get_ai_feedback(match_data, 2)
    except Exception as e:
        ai_feedback_p2 = f"AI feedback unavailable for Player 2: {e}"

    return render_template(
        'stats.html',
        stats=stats_data,
        ai_feedback_p1=ai_feedback_p1,
        ai_feedback_p2=ai_feedback_p2
    )

if __name__ == '__main__':
    app.run(debug=True)