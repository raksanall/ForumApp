import sqlite3

def create_tables():
    conn = sqlite3.connect('forum.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT NOT NULL,
        Email TEXT NOT NULL,
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Forums (
        ForumID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        Description TEXT,
        CreatedBy INTEGER,
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (CreatedBy) REFERENCES Users(UserID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Comments (
        CommentID INTEGER PRIMARY KEY AUTOINCREMENT,
        Content TEXT NOT NULL,
        CreatedBy INTEGER,
        ForumID INTEGER,
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (CreatedBy) REFERENCES Users(UserID),
        FOREIGN KEY (ForumID) REFERENCES Forums(ForumID)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
