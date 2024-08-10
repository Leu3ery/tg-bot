import sqlite3

class SqlHelper:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name
        self._initialize_database()
        self._initialize_database_members()

        
    def _initialize_database(self):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                nickname STRING,
                start_of_using_bot INTEGER,
                have_prime BOOLEAN,
                end_of_prime STRING,
                email STRING,
                end_of_timer STRING,
                had_prime BOOLEAN
            )""")
            conn.commit()
        print("Table created")
    
    def _initialize_database_members(self):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                end_of_prime STRING
            )""")
            conn.commit()
        print("Table created")
    
    def add_member(self, user_id, end_of_prime):
        # перезапиши данние в случаи если такой юзер уже есть иначе создание нового юзера
        if self.get_member(user_id):
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("UPDATE members SET end_of_prime = ? WHERE user_id = ?", (end_of_prime, user_id))
                conn.commit()
            return
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO members VALUES (?, ?, ?)", (None, user_id, end_of_prime))
            conn.commit()
    
    def get_all_members(self):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM members")
            return cur.fetchall()
        
    def get_member(self, user_id):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM members WHERE user_id = ?", (user_id,))
            return cur.fetchall()
        
    def del_member(self, user_id):  
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM members WHERE user_id = ?", (user_id,))
            conn.commit()
        
    def _get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def add_new_user(self, user_id):
        if self.get_user(user_id):
            print("User already exists")
            return
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (None, user_id, None, None, False, None, None, None, False))
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
        if self.get_user(user_id)[0][3] != None:
            print("Start of using bot already set")
            return
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
    
    def set_end_of_prime(self, user_id, end_of_prime):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET end_of_prime = ? WHERE user_id = ?", (end_of_prime, user_id))
            conn.commit()
        print("End of prime updated")

    def set_email(self, user_id, email):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET email = ? WHERE user_id = ?", (email, user_id))
            conn.commit()
        print("Email updated")
    
    def set_end_of_timer(self, user_id, end_of_timer):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET end_of_timer = ? WHERE user_id = ?", (end_of_timer, user_id))
            conn.commit()
        print("End of timer updated")
    
    def set_had_prime(self, user_id, had_prime):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET had_prime = ? WHERE user_id = ?", (had_prime, user_id))
            conn.commit()
        print("Had prime updated")

if __name__ == "__main__":
    db = SqlHelper(db_name='database.db')