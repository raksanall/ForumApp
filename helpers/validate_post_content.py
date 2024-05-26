# helpers/validate_post_content.py
def validate_post_content(content):
    # Post content should not be empty
    return bool(content.strip())
