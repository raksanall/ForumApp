Forum Application
This is a simple forum application built in Python.

Table of Contents
Overview
Requirements
Installation
Database Setup
Usage
Functions
Contributing
License
Overview
The Forum Application allows users to register, log in, create posts, comment on posts, and filter posts by username or keyword.

Requirements
To run the Forum Application, you need:

Python 3.x
SQLite
Installation
Clone this repository to your local machine.
Navigate to the project directory.
bash
Copy code
cd Forum_App
Install the required dependencies.
bash
Copy code
pip install -r requirements.txt
Database Setup
To set up the database for the Forum Application, you can create the necessary tables using SQLite. Below are the SQL commands to create each table:

Users Table
sql
Copy code
CREATE TABLE IF NOT EXISTS Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,
    Email TEXT NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
This table stores information about registered users including their username, email, and the timestamp of when they were created.

Forums Table
sql
Copy code
CREATE TABLE IF NOT EXISTS Forums (
    ForumID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Description TEXT,
    CreatedBy INTEGER,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CreatedBy) REFERENCES Users(UserID)
);
This table represents forums where users can create posts and discussions. It includes fields for the forum title, description, creator, and creation timestamp.

Comments Table
sql
Copy code
CREATE TABLE IF NOT EXISTS Comments (
    CommentID INTEGER PRIMARY KEY AUTOINCREMENT,
    Content TEXT NOT NULL,
    CreatedBy INTEGER,
    ForumID INTEGER,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CreatedBy) REFERENCES Users(UserID),
    FOREIGN KEY (ForumID) REFERENCES Forums(ForumID)
);
This table stores comments made by users on forum posts. It includes fields for the comment content, creator, associated forum ID, and creation timestamp.

To create these tables, you can execute the SQL commands using an SQLite client or integrate them into your Python code.

Usage
To start the Forum Application, run the following command:

bash
Copy code
python main.py
Functions
Here are the key functions provided by the Forum Application:

register_user(username, email, password): Registers a new user with the given username, email, and password.
login(email, password): Logs in a user with the given email and password.
add_post(title, content, user_id): Adds a new post with the given title, content, and user ID.
delete_post(post_id, user_id): Deletes a post with the specified ID if the user ID matches the creator of the post.
update_post(post_id, user_id, new_title, new_content): Updates the title and content of a post with the specified ID if the user ID matches the creator of the post.
add_comment(content, user_id, post_id): Adds a new comment with the given content, user ID, and post ID.
Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.