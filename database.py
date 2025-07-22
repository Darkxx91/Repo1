import sqlite3

DATABASE = 'database.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        db.executescript(f.read())
    db.commit()

def get_user(username):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    db.close()
    return user

def create_user(username, password):
    db = get_db()
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    db.commit()
    db.close()

def subscribe_user(username):
    db = get_db()
    db.execute('UPDATE users SET subscribed = 1 WHERE username = ?', (username,))
    db.commit()
    db.close()

if __name__ == '__main__':
    init_db()
