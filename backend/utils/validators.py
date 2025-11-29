"""
Input validation utilities
"""

import re
import base64


def validate_audio_data(data):
    """
    Validate audio data from client

    Args:
        data: Dictionary containing audio data

    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(data, dict):
        return False

    if 'audio' not in data:
        return False

    audio = data['audio']

    # Check if it's a valid base64 string
    if not isinstance(audio, str):
        return False

    try:
        # Try to decode base64
        base64.b64decode(audio)
        return True
    except Exception:
        return False


def validate_session_id(session_id, active_sessions):
    """
    Validate session ID exists in active sessions

    Args:
        session_id: Session ID to validate
        active_sessions: Dictionary of active sessions

    Returns:
        bool: True if valid, False otherwise
    """
    if not session_id:
        return False

    if not isinstance(session_id, str):
        return False

    return session_id in active_sessions


def sanitize_filename(filename):
    """
    Sanitize filename to prevent path traversal attacks

    Args:
        filename: Original filename

    Returns:
        str: Sanitized filename
    """
    if not filename:
        return "unknown"

    # Remove any path separators
    filename = filename.replace('/', '_').replace('\\', '_')

    # Remove any non-alphanumeric characters except underscore, dash, and dot
    filename = re.sub(r'[^a-zA-Z0-9_\-.]', '', filename)

    # Limit length
    if len(filename) > 255:
        filename = filename[:255]

    return filename


def validate_api_key(api_key, key_name="API_KEY"):
    """
    Validate API key is not empty or placeholder

    Args:
        api_key: API key to validate
        key_name: Name of the key (for error messages)

    Returns:
        bool: True if valid

    Raises:
        ValueError: If invalid
    """
    if not api_key:
        raise ValueError(f"{key_name} is not set")

    if api_key.startswith('your_') or api_key.endswith('_here'):
        raise ValueError(f"{key_name} appears to be a placeholder")

    if len(api_key) < 10:
        raise ValueError(f"{key_name} is too short")

    return True
