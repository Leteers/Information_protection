import sqlite3

class Connection():
    def __init__(self) -> None:
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS votes(vote TEXT, sign BIGINT);")
    def push(self, vote, sign):
        self.cursor.execute(f"INSERT INTO votes(vote,sign) VALUES ('{vote}',{sign})")
        self.connection.commit()
    def get_results(self):
        self.cursor.execute("SELECT vote, count(*) from votes group by vote")
        return (self.cursor.fetchall())