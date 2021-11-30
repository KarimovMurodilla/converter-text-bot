@bot.message_handler(commands = ['start'])
def language_selection(message):
    with sql.connect('tele_list_bot.db') as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXiSTS users(
                    user_name TEXT,
                    id INTEGER)''')
        con.commit()

        cur.execute("SELECT * FROM users WHERE id = ?", (message.from_user.id,))
        if not cur.fetchall():
            cur.execute("INSERT INTO users (user_name, id)VALUES(?, ?)",
                (message.from_user.first_name, message.from_user.id))
            con.commit()