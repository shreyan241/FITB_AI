import re

def sanitize_text(text: str) -> str:
    """Remove all non-alphanumeric characters and convert to lowercase."""
    if not text:
        return ""
    # Remove all non-alphanumeric characters and convert to lowercase
    sanitized = re.sub(r'[^a-zA-Z0-9]', '', text)
    return sanitized.lower()