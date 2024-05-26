import sqlite3

class ForumApp:
    def __init__(self, db_name='forum.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row

    def add_user(self, username, email):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Users (Username, Email) VALUES (?, ?)", (username, email))
        self.conn.commit()
        return cursor.lastrowid

    def add_forum(self, title, description, created_by):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Forums (Title, Description, CreatedBy) VALUES (?, ?, ?)", (title, description, created_by))
        self.conn.commit()
        return cursor.lastrowid

    def add_comment(self, content, created_by, forum_id):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Comments (Content, CreatedBy, ForumID) VALUES (?, ?, ?)", (content, created_by, forum_id))
        self.conn.commit()
        return cursor.lastrowid

    def get_user_forums(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Forums WHERE CreatedBy = ?", (user_id,))
        return cursor.fetchall()

    def get_forum_comments(self, forum_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Comments WHERE ForumID = ?", (forum_id,))
        return cursor.fetchall()

    def get_statistics(self):
        cursor = self.conn.cursor()
        user_count = cursor.execute("SELECT COUNT(*) FROM Users").fetchone()[0]
        forum_count = cursor.execute("SELECT COUNT(*) FROM Forums").fetchone()[0]
        comment_count = cursor.execute("SELECT COUNT(*) FROM Comments").fetchone()[0]
        return {
            'user_count': user_count,
            'forum_count': forum_count,
            'comment_count': comment_count
        }
