class UsuarioException(Exception):
    """Exceção base para regras de negócio de usuário."""
    pass


class UsuarioDuplicadoException(UsuarioException):
    """Lançada quando a matrícula ou o e-mail já estão cadastrados."""
    pass


class DadosUsuarioInvalidosException(UsuarioException):
    """Lançada quando campos obrigatórios estão vazios ou inválidos."""
    pass