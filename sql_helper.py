import sqlite3

class SqlHelper:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name
        self._initialize_database()
        
    def _initialize_database(self):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                nickname STRING,
                start_of_using_bot INTEGER,
                have_prime BOOLEAN,
                email STRING
            )""")
            conn.commit()
        print("Table created")

    def _get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def add_new_user(self, user_id):
        if self.get_user(user_id):
            print("User already exists")
            return
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (None, user_id, None, None, False, None))
            conn.commit()
        print("User added")
    
    def get_user(self, user_id):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            return cur.fetchall()
    
    def get_all_users(self):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")
            return cur.fetchall()
    
    def set_nickname(self, user_id, nickname):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET nickname = ? WHERE user_id = ?", (nickname, user_id))
            conn.commit()
        print("Nickname updated")

    def set_start_of_using_bot(self, user_id, start_of_using_bot):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET start_of_using_bot = ? WHERE user_id = ?", (start_of_using_bot, user_id))
            conn.commit()
        print("Start of using bot updated")

    def set_have_prime(self, user_id, have_prime: bool):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET have_prime = ? WHERE user_id = ?", (have_prime, user_id))
            conn.commit()
        print("Have prime updated")

    def set_email(self, user_id, email):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET email = ? WHERE user_id = ?", (email, user_id))
            conn.commit()
        print("Email updated")

if __name__ == "__main__":
    db = SqlHelper(db_name='database.db')