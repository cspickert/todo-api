from todo.utils import generate_key


def test_generate_key():
    key = generate_key()
    assert len(key) == 32
