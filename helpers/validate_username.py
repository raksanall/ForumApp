# helpers/validate_username.py

def validate_username(username):
    # Username should contain only alphanumeric characters and underscores
    return username.isalnum() and '_' not in username
