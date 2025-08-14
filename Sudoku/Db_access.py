import sqlite3

def initiate():
    with sqlite3.connect("Sudoko.db") as con:
        cur = con.cursor()

        cur.execute("CREATE TABLE LeaderboardSudoko (Username text, Time text)")
        
def addEvent(Username, Time):
    with sqlite3.connect("Sudoko.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO LeaderboardSudoko VALUES(?, ?)", (Username, Time))

def getLeaderboard():
    with sqlite3.connect("Sudoko.db") as con:
        cur = con.cursor()

        leaderboardList = list(cur.execute("SELECT * FROM LeaderboardSudoko ORDER BY Time ASC"))
        
    return leaderboardList[:5]


if __name__ == '__main__':
    
    with sqlite3.connect("Sudoko.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM LeaderboardSudoko")
        #x = cur.execute("SELECT Username, Time FROM LeaderboardSudoko")
        #print(list(x))
