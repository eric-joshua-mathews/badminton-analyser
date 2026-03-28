import sqlite3
from symbol import continue_stmt

def get_db_connection():
    conn = sqlite3.connect("data/badminton.db")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def get_or_create_player(name):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT PlayerID FROM Players WHERE Name = ?", (name,))
    row = cur.fetchone()

    if row:
        player_id = row["PlayerID"]
    else:
        cur.execute("INSERT INTO Players (Name) VALUES (?)", (name,))
        conn.commit()
        player_id = cur.lastrowid

    conn.close()
    return player_id
def create_match(player1_id,player2_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO Matches(playerOneID,playerTwoID,WinnerID) Values(?,?,NULL)
    """,(player1_id,player2_id,))
    return cur.lastrowid
def insert_rally(match_id,rally_data,player1_id,player2_id):
    with get_db_connection() as conn:
        cur = conn.cursor()

        rally_winnerID=player1_id if rally_data["winner"]==1 else player2_id #making sure to use session ID instead of 1 or 2
        server_id=player1_id if rally_data["server"]==1 else player2_id
        cur.execute("""SELECT COUNT(*) As count FROM Rally
        WHERE MatchID = ?""", (match_id,))
        rally_num = cur.fetchone()["count"]+1
        cur.execute("""INSERT INTO Rally(MatchID, ServerID,RallyWinnerID,RallyNum)
        Values(?,?,?,?)
        """,(match_id,server_id,rally_winnerID,rally_num))
        rally_id=cur.lastrowid
        for i,shot in enumerate(rally_data["rally"],start=1):
            true_player_id=player1_id if shot["Player"]==1 else player2_id
            is_final = int(shot.get("isFinal",False))
            shot_name = shot["shotType"]

            cur.execute("""SELECT ShotTypeID FROM ShotType WHERE ShotTypeName=?""",(shot_name,))
            row = cur.fetchone()
            if row:
                shot_type_id = row["ShotTypeID"]
            else:
                cur.execute("""INSERT INTO ShotType(ShotTypeName) VALUES (?)""",(shot_name,))
                shot_type_id = cur.lastrowid
            cur.execute("""
            INSERT INTO Shots (RallyID, PlayerID,ShotTypeID,ShotOrder,isFINAL)
            Values(?,?,?,?,?)""",
                        (rally_id,true_player_id,shot_type_id,i,is_final)
            )
        return rally_id