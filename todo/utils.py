from django.utils.crypto import get_random_string


def generate_key() -> str:
    """Returns a securely generated random 32-character string."""

    return get_random_string(length=32)


__all__ = ["generate_key"]
