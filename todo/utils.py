import uuid


def generate_key() -> str:
    """Returns a randomly generated 32-character string."""

    return uuid.uuid4().hex
