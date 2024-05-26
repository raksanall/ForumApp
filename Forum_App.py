from helpers.auth_helper import hash_password, check_password
from helpers.db_helper import DatabaseHelper
from helpers.validate_email import validate_email
from helpers.validate_password import validate_password
from helpers.validate_username import validate_username
from helpers.validate_post_content import validate_post_content
from helpers.validate_comment_content import validate_comment_content
from entities.comment import Comment
from entities.forum import Forum
from entities.user import User
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

    def filter_posts_by_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT Posts.PostID, Posts.Title, Posts.Content, Posts.CreatedAt, Users.Username
        FROM Posts
        JOIN Users ON Posts.UserID = Users.UserID
        WHERE Users.Username = ?
        ''', (username,))
        return cursor.fetchall()
    
    def get_member_list(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT Username FROM Users")
        members = cursor.fetchall()
        return members
    
    def filter_posts_by_keyword(self, keyword):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT Posts.PostID, Posts.Title, Posts.Content, Posts.CreatedAt, Users.Username
        FROM Posts
        JOIN Users ON Posts.UserID = Users.UserID
        WHERE Posts.Title LIKE ? OR Posts.Content LIKE ?
        ''', (f'%{keyword}%', f'%{keyword}%'))
        return cursor.fetchall()
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
    
    def check_user_post(self, post_id, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Posts WHERE PostID = ? AND UserID = ?", (post_id, user_id))
        post = cursor.fetchone()
        return post is not None

    def update_post(self, post_id, user_id, new_title, new_content):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE Posts SET Title = ?, Content = ? WHERE PostID = ? AND UserID = ?", (new_title, new_content, post_id, user_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
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
