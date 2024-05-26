import sqlite3
import bcrypt

class ForumApp:
    def __init__(self, db_name='forum.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Posts (
            PostID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Content TEXT NOT NULL,
            UserID INTEGER,
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Comments (
            CommentID INTEGER PRIMARY KEY AUTOINCREMENT,
            Content TEXT NOT NULL,
            UserID INTEGER NOT NULL,
            PostID INTEGER NOT NULL,
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (PostID) REFERENCES Posts(PostID)
        )
        ''')

        self.conn.commit()


    def register_user(self, username, email, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Email = ?", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return None

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO Users (Username, Email, Password) VALUES (?, ?, ?)", (username, email, hashed_password))
        self.conn.commit()
        return cursor.lastrowid

    def login(self, email, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Email = ?", (email,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['Password']):
            return user['UserID']
        return None

    def add_post(self, title, content, user_id):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Posts (Title, Content, UserID) VALUES (?, ?, ?)", (title, content, user_id))
        self.conn.commit()
        return cursor.lastrowid

    def delete_post(self, post_id, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Posts WHERE PostID = ? AND UserID = ?", (post_id, user_id))
        post = cursor.fetchone()
        if post:
            cursor.execute("DELETE FROM Posts WHERE PostID = ?", (post_id,))
            self.conn.commit()
            return True
        return False

    def get_user_posts(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Posts WHERE UserID = ?", (user_id,))
        return cursor.fetchall()

    def get_all_posts(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT Posts.PostID, Posts.Title, Posts.Content, Posts.CreatedAt, Users.Username
        FROM Posts
        JOIN Users ON Posts.UserID = Users.UserID
        ''')
        return cursor.fetchall()

    def add_comment(self, content, user_id, post_id):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Comments (Content, UserID, PostID) VALUES (?, ?, ?)", (content, user_id, post_id))
        self.conn.commit()
        return cursor.lastrowid

    def get_comments_for_post(self, post_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT Comments.CommentID, Comments.Content, Comments.CreatedAt, Users.Username
        FROM Comments
        JOIN Users ON Comments.UserID = Users.UserID
        WHERE Comments.PostID = ?
        ''', (post_id,))
        return cursor.fetchall()
