# helpers/validate_password.py
def validate_password(password):
    # Password length should be at least 8 characters
    return len(password) >= 8
