from Forum_App import ForumApp
from helpers.validate_email import validate_email
from helpers.validate_password import validate_password
from helpers.validate_username import validate_username
from helpers.validate_post_content import validate_post_content
from helpers.validate_comment_content import validate_comment_content

GREEN = '\033[92m'  # Green color
ORANGE = '\033[38;5;208m'
PURPLE = '\033[95m'
RESET = '\033[0m'   # Reset color
ESC = chr(27)

def main():
    app = ForumApp()

    while True:
        # Display member list
        print()
        print(f"{ESC}[31;47m {ORANGE} Member List : {RESET}")
        members = app.get_member_list()
        print()
        print(f"Number of users: {len(members)}")
        print()
        for member in members:
            print(f"Username: {member['Username']}")
            
        print("\n")
        print(f"{ESC}[31;47m {ORANGE} All Posts : {RESET}")
        print("\n")
        all_posts = app.get_all_posts()
        for post in all_posts:
            print(f"ID: {post['PostID']}:{GREEN} {post['Title']}:{RESET} \n Content: {post['Content']}, CreatedAt: {post['CreatedAt']}, Creator: {post['Username']}")
            
            # Display comments for each post
            post_id = post['PostID']
            comments = app.get_comments_for_post(post_id)
            if comments:
                print("Comments:")
                for comment in comments:
                    print(f"[{PURPLE}CommentID: {comment['CommentID']}{RESET}, Username: {comment['Username']}, Content: {comment['Content']}, CreatedAt: {comment['CreatedAt']}]")
            else:
                print(f"[{PURPLE}No comments]{RESET}")
            print("\n")
        
       
        print(f"{ESC}[31;47m  -- MENU --  {RESET}")
        print()
        print(f"{ESC}[31;47m [1] Register      {RESET}")
        print()
        print(f"{ESC}[31;47m [2] Login         {RESET}")
        print()
        print(f"{ESC}[31;47m [3] Filter Posts  {RESET}")
        print()
        print(f"{ESC}[31;47m [4] Exit          {RESET}")
        print()

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == '1':
            # Registration
            username = input("Enter your username: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")

            # Validate inputs
            if not validate_username(username):
                print("Invalid username! Username should contain only alphanumeric characters and no underscores.")
                continue
            if not validate_email(email):
                print("Invalid email address!")
                continue
            if not validate_password(password):
                print("Invalid password! Password should be at least 8 characters long.")
                continue

            user_id = app.register_user(username, email, password)
            if user_id:
                print("User registration successful!")
            else:
                print("User registration failed. User with this email already exists.")
        elif choice == '2':
            # Login
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            user_id = app.login(email, password)
            if user_id:
                print(f"{ESC}[34;42m Login successful! {RESET}")
        
                # Display member list
                print()
                print(f"{ESC}[31;47m {ORANGE} Member List : {RESET}")
                members = app.get_member_list()
                print()
                print(f"Number of users: {len(members)}")
                print()
                for member in members:
                    print(f"Username: {member['Username']}")

                while True:
                    user_posts = app.get_user_posts(user_id)
                    print("Your Posts:")
                    for post in user_posts:
                        print(f"ID: {post['PostID']}, Title: {post['Title']}, Content: {post['Content']}, CreatedAt: {post['CreatedAt']}")
                        post_id = post['PostID']
                        comments = app.get_comments_for_post(post_id)
                        if comments:
                            print("Comments:")
                            for comment in comments:
                                print(f"[{PURPLE}CommentID: {comment['CommentID']}{RESET}, Username: {comment['Username']}, Content: {comment['Content']}, CreatedAt: {comment['CreatedAt']}]")
                        else:
                            print(f"[{PURPLE}No comments]{RESET}")
                        print("\n")
            
                    print(f"{ESC}[31;47m  -- MENU --  {RESET}")
                    print("1. Add a comment")
                    print("2. Add a post")
                    print("3. Delete a post")
                    print("4. Update a post")
                    print("5. Filter Posts")
                    print("6. Logout")
        
                    choice = input("Enter your choice (1/2/3/4/5/6): ").strip()
        
                    if choice == '1':
                        # Add a comment
                        # Existing code...
                        pass
                    elif choice == '2':
                        # Add a post
                        # Existing code...
                        pass
                    elif choice == '3':
                        # Delete a post
                        # Existing code...
                        pass
                    elif choice == '4':
                        # Update a post
                        # Existing code...
                        pass
                    elif choice == '5':
                        # Filter posts
                        print("\nFilter Posts:")
                        print("1. By Username")
                        print("2. By Keyword")
                        filter_choice = input("Enter your choice (1/2): ").strip()
                        if filter_choice == '1':
                            username = input("Enter the username: ")
                            filtered_posts = app.filter_posts_by_user(username)
                            if filtered_posts:
                                for post in filtered_posts:
                                    print(f"ID: {post['PostID']}:{GREEN} {post['Title']}:{RESET} \n Content: {post['Content']}, CreatedAt: {post['CreatedAt']}, Creator: {post['Username']}")
                            else:
                                print("No posts found for this user.")
                        elif filter_choice == '2':
                            keyword = input("Enter the keyword: ")
                            filtered_posts = app.filter_posts_by_keyword(keyword)
                            if filtered_posts:
                                for post in filtered_posts:
                                    print(f"ID: {post['PostID']}:{GREEN} {post['Title']}:{RESET} \n Content: {post['Content']}, CreatedAt: {post['CreatedAt']}, Creator: {post['Username']}")
                            else:
                                print("No posts found with this keyword.")
                        else:
                            print("Invalid choice. Please enter a number between 1 and 2.")
                    elif choice == '6':
                        # Logout
                        print("Logout successful!")
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 6.")
            else:
                print("Login failed. Invalid email or password.")
        elif choice == '3':
            print("\nFilter Posts:")
            print("1. By Username")
            print("2. By Keyword")
            filter_choice = input("Enter your choice (1/2): ").strip()
            if filter_choice == '1':
                username = input("Enter the username: ")
                filtered_posts = app.filter_posts_by_user(username)
                if filtered_posts:
                    for post in filtered_posts:
                        print(f"ID: {post['PostID']}:{GREEN} {post['Title']}:{RESET} \n Content: {post['Content']}, CreatedAt: {post['CreatedAt']}, Creator: {post['Username']}")
                else:
                    print("No posts found for this user.")
            elif filter_choice == '2':
                keyword = input("Enter the keyword: ")
                filtered_posts = app.filter_posts_by_keyword(keyword)
                if filtered_posts:
                    for post in filtered_posts:
                        print(f"ID: {post['PostID']}:{GREEN} {post['Title']}:{RESET} \n Content: {post['Content']}, CreatedAt: {post['CreatedAt']}, Creator: {post['Username']}")
                else:
                    print("No posts found with this keyword.")
            else:
                print("Invalid choice. Please enter a number between 1 and 2.")
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
