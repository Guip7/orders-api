from app.core.security import hash_password, verify_password


def test_hash_is_not_the_plain_password() -> None:
    hashed = hash_password("abc12345")

    assert hashed != "abc12345"
    assert hashed.startswith("$argon2id$")


def test_verify_accepts_correct_password() -> None:
    hashed = hash_password("abc12345")

    assert verify_password("abc12345", hashed) is True


def test_verify_rejects_wrong_password() -> None:
    hashed = hash_password("abc12345")

    assert verify_password("errada123", hashed) is False


def test_same_password_generates_different_hashes() -> None:
    assert hash_password("abc12345") != hash_password("abc12345")


def test_verify_returns_false_for_invalid_hash() -> None:
    assert verify_password("abc12345", "isso-nao-e-um-hash") is False
