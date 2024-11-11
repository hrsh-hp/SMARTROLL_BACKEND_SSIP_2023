import time
import uuid

def generate_unique_hash():
    """
    Generates a more robust unique slug using a larger portion of UUID and timestamp.
    """
    # Use a larger part of UUID (32 characters) and append a timestamp for uniqueness
    random_hash = str(uuid.uuid4().hex)[:16]  # Using 16 characters from the UUID
    timestamp = str(int(time.time() * 1000))  # Millisecond precision timestamp
    
    # Combine UUID and timestamp for a more robust unique hash
    unique_hash = f"{random_hash}_{timestamp}"
    
    return unique_hash