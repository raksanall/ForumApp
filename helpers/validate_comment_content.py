# helpers/validate_comment_content.py
def validate_comment_content(content):
    # Comment content should not be empty
    return bool(content.strip())
