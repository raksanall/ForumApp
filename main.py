from Forum_App import ForumApp

GREEN = '\033[92m'  # Green color
ORANGE = '\033[38;5;208m'
PURPLE = '\033[95m'
RESET = '\033[0m'   # Reset color

def main():
    app = ForumApp()

    # Display all posts
    print("\n")
    print(f"{ORANGE}All Posts:{RESET}")
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
        
    # Prompt the user for registration or login
    choice = input("Do you want to (R)egister or (L)ogin? ").strip().lower()

    if choice == 'r':
        # Registration
        username = input("Enter your username: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        user_id = app.register_user(username, email, password)
        if user_id:
            print("User registration successful!")
        else:
            print("User registration failed. User with this email already exists.")
    elif choice == 'l':
        # Login
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        user_id = app.login(email, password)
        if user_id:
            print("Login successful!")
            while True:
                # Display user's own posts
                user_posts = app.get_user_posts(user_id)
                print("Your Posts:")
                for post in user_posts:
                    print(f"ID: {post['PostID']}, Title: {post['Title']}, Content: {post['Content']}, CreatedAt: {post['CreatedAt']}")
                    
                    # Display comments for user's own posts
                    post_id = post['PostID']
                    comments = app.get_comments_for_post(post_id)
                    if comments:
                        print("Comments:")
                        for comment in comments:
                            print(f"[{PURPLE}CommentID: {comment['CommentID']}{RESET}, Username: {comment['Username']}, Content: {comment['Content']}, CreatedAt: {comment['CreatedAt']}]")
                    else:
                        print(f"[{PURPLE}No comments]{RESET}")
                    print("\n")
            
                # Display menu options
                print("\nMenu:")
                print("1. Add a comment")
                print("2. Add a post")
                print("3. Delete a post")
                print("4. Logout")
            
                choice = input("Enter your choice (1/2/3/4): ").strip()
            
                if choice == '1':
                    # Add a comment
                    post_id = input("Enter the ID of the post you want to add a comment to: ")
                    content = input("Enter your comment: ")
                    comment_id = app.add_comment(content, user_id, post_id)
                    if comment_id:
                        print("Comment added successfully!")
                    else:
                        print("Failed to add comment.")
                elif choice == '2':
                    # Add a post
                    title = input("Enter the title of your post: ")
                    content = input("Enter the content of your post: ")
                    post_id = app.add_post(title, content, user_id)
                    if post_id:
                        print("Post added successfully with ID:", post_id)
                    else:
                        print("Failed to add post.")
                elif choice == '3':
                    # Delete a post
                    post_id = input("Enter the ID of the post you want to delete: ")
                    if app.delete_post(post_id, user_id):
                        print("Post deleted successfully.")
                    else:
                        print("Failed to delete post.")
                elif choice == '4':
                    # Logout
                    print("Logout successful!")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")
        else:
            print("Login failed. Invalid email or password.")
    else:
        print("Invalid choice. Please choose 'R' for registration or 'L' for login.")


if __name__ == "__main__":
    main()
