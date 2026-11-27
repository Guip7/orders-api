class EmailAlreadyRegisteredError(Exception):
    """Já existe um usuário com este e-mail."""

    def __init__(self, email: str) -> None:
        super().__init__(f"email already registered: {email}")
        self.email = email


class InvalidTokenError(Exception):
    """Token malformado, com assinatura inválida ou do tipo errado."""


class TokenExpiredError(InvalidTokenError):
    """Token válido, porém expirado."""
