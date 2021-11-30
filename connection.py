import sqlite3 as sql


with sql.connect("users.db", check_same_thread=False) as con:
    cur = con.cursor()


def createTable():
    cur.execute("""CREATE TABLE IF NOT EXISTS activeUsers(
                user_id INT,
                user_lang TEXT)""")
    con.commit()


def checkUser(user_id: str):
    checkUser = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    return checkUser


def reg_user(user_id: str):
    cur.execute("INSERT INTO users (user_id)VALUES(?)", (user_id,))
    con.commit()


def checkLang(user_id: str):
    userLang = cur.execute("SELECT user_lang FROM users WHERE user_id = ?", (user_id,)).fetchone()
    return userLang

def setLang(user_id: str, user_lang: str):
    cur.execute("UPDATE users SET user_lang = ? WHERE user_id = ?", (user_lang, user_id,))
    con.commit()


def copy():
    cur.execute("INSERT INTO activeUsers SELECT * FROM users")
    con.commit()


def deleteUser(user_id):
    cur.execute("DELETE FROM activeUsers WHERE user_id = ?", (user_id,))
    con.commit()
