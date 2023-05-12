# Import sqlite 3
import sqlite3

class Notification:
    def __init__(self,id, username, date_time, notify):
        self.id = id
        self.username = username
        self.date_time = date_time
        self.notify = notify

    def saveNotify(self, message, date_time):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        q1 = "CREATE TABLE IF NOT EXISTS notification (id INTEGER PRIMARY KEY, username TEXT,time TEXT, notify TEXT)"
        cursor.execute(q1)
        q2 = "INSERT INTO notification VALUES(NULL,?,?,?)"
        cursor.execute(q2, ("THANH NHAN", message, date_time))
        conn.commit()
        conn.close()

    def getNotify(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        sqlite_select_query = """SELECT * from notification"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        return records

    def deleteAllRecords(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM notification;', )
        conn.commit()
        conn.close()

    def deleteTable(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("DROP TABLE notification")
        conn.commit()
        conn.close()
