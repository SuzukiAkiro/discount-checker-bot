import sqlite3 as sqlite

class BotDB():
    def __init__(self, db_file):
        self.db = sqlite.connect(db_file)
        self.cursor = self.db.cursor()
        try:
            self.db.execute("""
                            CREATE TABLE IF NOT EXISTS users(
                                user_id integer not null primary key,
                                username text
                                )
                            """)
            self.db.execute("""
                            CREATE TABLE IF NOT EXISTS watchlists(
                                id integer not null primary key,
                                owner integer,
                                FOREIGN KEY(owner) REFERENCES users(user_id)
                                )
                            """)
            self.db.commit()
        except sqlite.Error as e:
            print(f"Error: {e}")


    def user_exists(self, user_id):
        cursor = self.db.execute("SELECT * FROM users where user_id={id}".format(id=user_id))
        return bool(cursor.fetchall())


    def create_user(self, user_id, user_name):
            try:
                if not self.user_exists(user_id):
                    self.db.execute("""
                                          INSERT INTO users VALUES ({id},'{name}')""".format(id=user_id, name=user_name)
                                          )
                    self.db.commit()
                else:
                    print('User exists!')
            except sqlite.Error as e:
                print(f"Error: {e}")

    def create_wailtist(self, user_id):
        self.db.execute("""
                        INSERT INTO waitlists (user_id) VALUES (id)
                        """.format(id=user_id))
    def close_db(self):
        self.cursor.close()
