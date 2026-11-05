class EmailAlreadyRegisteredError(Exception):
    """Já existe um usuário com este e-mail."""

    def __init__(self, email: str) -> None:
        super().__init__(f"email already registered: {email}")
        self.email = email
