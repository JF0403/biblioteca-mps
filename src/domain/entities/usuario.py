from abc import ABC
from src.domain.exceptions.usuario_exceptions import DadosUsuarioInvalidosException


class Usuario(ABC):
    def __init__(self, matricula: str, nome: str, email: str, limite_livros: int):
        self._validar_dados(matricula, nome, email)
        self.matricula = matricula.strip()
        self.nome = nome.strip()
        self.email = email.strip()
        self.limite_livros = limite_livros

    @staticmethod
    def _validar_dados(matricula: str, nome: str, email: str) -> None:
        if not matricula or not matricula.strip():
            raise DadosUsuarioInvalidosException("A matrícula não pode ser vazia.")
        if not nome or not nome.strip():
            raise DadosUsuarioInvalidosException("O nome não pode ser vazio.")
        if not email or "@" not in email:
            raise DadosUsuarioInvalidosException("O e-mail informado é inválido.")

    def obter_tipo(self) -> str:
        return self.__class__.__name__


class Aluno(Usuario):
    LIMITE_LIVROS_PADRAO = 3

    def __init__(self, matricula: str, nome: str, email: str):
        super().__init__(
            matricula=matricula,
            nome=nome,
            email=email,
            limite_livros=self.LIMITE_LIVROS_PADRAO
        )


class Professor(Usuario):
    LIMITE_LIVROS_PADRAO = 5

    def __init__(self, matricula: str, nome: str, email: str):
        super().__init__(
            matricula=matricula,
            nome=nome,
            email=email,
            limite_livros=self.LIMITE_LIVROS_PADRAO
        )