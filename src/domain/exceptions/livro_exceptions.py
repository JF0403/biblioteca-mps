class LivroException(Exception):
    """Exceção base para regras de negócio de Livro."""
    pass


class LivroDuplicadoException(LivroException):
    """Lançada quando já existe um livro cadastrado com o mesmo ISBN."""
    pass


class LivroNaoEncontradoException(LivroException):
    """Lançada quando uma operação referencia um ISBN inexistente."""
    pass


class LivroInvalidoException(LivroException):
    """Lançada quando dados obrigatórios do livro estão vazios ou inválidos."""
    pass