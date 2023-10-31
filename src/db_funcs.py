import sqlite3 as sqlite


class BotDB:
    def __init__(self, db_file):
        self.db = sqlite.connect(db_file)
        self.cursor = self.db.cursor()
        try:
            self.db.execute(
                """
                            CREATE TABLE IF NOT EXISTS users(
                                user_id integer not null primary key,
                                username text
                                )
                            """
            )
            self.db.execute(
                """
                            CREATE TABLE IF NOT EXISTS watchlists(
                                id integer not null primary key,
                                owner integer,
                                FOREIGN KEY(owner) REFERENCES users(user_id)
                                )
                            """
            )
            self.db.execute(
                """
                            CREATE TABLE IF NOT EXISTS items(
                                id integer not null primary key,
                                watchlist_id integer,
                                url text,
                                price real,
                                FOREIGN KEY(watchlist_id) REFERENCES watchlists(id)

                                )
                            """
            )
            self.db.commit()
        except sqlite.Error as e:
            print(f"Error: {e}")

    def user_exists(self, user_id):
        cursor = self.db.execute(
            "SELECT * FROM users where user_id={id}".format(id=user_id)
        )
        return bool(cursor.fetchall())

    def add_user(self, user_id, user_name):
        try:
            if not self.user_exists(user_id):
                self.db.execute(
                    """
                                          INSERT INTO users VALUES ({id},'{name}')""".format(
                        id=user_id, name=user_name
                    )
                )
                self.db.commit()
            else:
                print("User exists!")
        except sqlite.Error as e:
            print(f"Error: {e}")

    def watchlist_exists(self, user_id):
        cursor = self.db.execute(
            "SELECT * FROM watchlists where owner={id}".format(id=user_id)
        )
        return bool(cursor.fetchall())

    def init_watchlist(self, user_id):
        try:
            if not self.watchlist_exists(user_id):
                self.db.execute(
                    """
                                INSERT INTO watchlists (owner) VALUES ({id})
                                """.format(
                        id=user_id
                    )
                )
                self.db.commit()
            else:
                print("Waitlist exist!")
        except sqlite.Error as e:
            print(f"error: {e}")

    def find_user_watchlist(self, user_id):
        watchlist_id = self.db.execute(
            """SELECT id FROM watchlists WHERE owner='{owner_id}'""".format(
                owner_id=user_id
            )
        )
        return watchlist_id.fetchone()

    def parse_watchlist(self, user_id):
        try:
            cursor = self.db.execute(
                """
                                     SELECT url, price FROM items WHERE watchlist_id={wl_id}
                                     """.format(
                    wl_id=self.find_user_watchlist(user_id)
                )
            ).fetchall()
            return cursor
        except sqlite.Error as e:
            print(f"Error: {e}")

    def add_item(self, url, user_id):
        try:
            wl_id = self.find_user_watchlist(user_id)
            self.db.execute(
                """
                            INSERT INTO items (url, watchlist_id) VALUE `{url}`, `{watchlist}`
                            """.format(
                    url=url, watchlist=wl_id
                )
            )
            self.db.commit()
        except sqlite.Error as e:
            print(f"Error: {e}")

    def close_db(self):
        self.cursor.close()
