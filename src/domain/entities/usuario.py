import re
from abc import ABC
from src.domain.exceptions.usuario_exceptions import (
    DadosUsuarioInvalidosException,
    LoginInvalidoException,
    SenhaFracaException,
)


class Usuario(ABC):
    def __init__(self, matricula: str, nome: str, email: str, login: str, senha: str, limite_livros: int):
        self._validar_dados_gerais(matricula, nome, email)
        self._validar_login(login)
        self._validar_senha(senha, login)

        self.matricula = matricula.strip()
        self.nome = nome.strip()
        self.email = email.strip()
        self.login = login.strip()
        self.senha = senha
        self.limite_livros = limite_livros

    @staticmethod
    def _validar_dados_gerais(matricula: str, nome: str, email: str) -> None:
        if not matricula or not matricula.strip():
            raise DadosUsuarioInvalidosException("A matrícula não pode ser vazia.")
        if not nome or not nome.strip():
            raise DadosUsuarioInvalidosException("O nome não pode ser vazio.")
        if not email or "@" not in email:
            raise DadosUsuarioInvalidosException("O e-mail informado é inválido.")

    @staticmethod
    def _validar_login(login: str) -> None:
        if not login or not login.strip():
            raise LoginInvalidoException("O login não pode ser vazio.")
        login_limpo = login.strip()
        if len(login_limpo) > 12:
            raise LoginInvalidoException("O login deve ter no máximo 12 caracteres.")
        if any(char.isdigit() for char in login_limpo):
            raise LoginInvalidoException("O login não pode conter números.")

    @staticmethod
    def _validar_senha(senha: str, login: str) -> None:
        if not senha or len(senha) < 8:
            raise SenhaFracaException("A senha deve ter no mínimo 8 caracteres (política AWS IAM).")
        if not re.search(r"[A-Z]", senha):
            raise SenhaFracaException("A senha deve conter ao menos uma letra maiúscula.")
        if not re.search(r"[a-z]", senha):
            raise SenhaFracaException("A senha deve conter ao menos uma letra minúscula.")
        if not re.search(r"[0-9]", senha):
            raise SenhaFracaException("A senha deve conter ao menos um número.")
        caracteres_especiais = "!@#$%^&*()_+-=[]{}|':;,.<>?/~`"
        if not any(char in caracteres_especiais for char in senha):
            raise SenhaFracaException("A senha deve conter ao menos um caractere especial.")
        if login and senha.strip().lower() == login.strip().lower():
            raise SenhaFracaException("A senha não pode ser igual ao login.")

    def obter_tipo(self) -> str:
        return self.__class__.__name__


class Aluno(Usuario):
    LIMITE_LIVROS_PADRAO = 3

    def __init__(self, matricula: str, nome: str, email: str, login: str, senha: str):
        super().__init__(matricula, nome, email, login, senha, self.LIMITE_LIVROS_PADRAO)


class Professor(Usuario):
    LIMITE_LIVROS_PADRAO = 5

    def __init__(self, matricula: str, nome: str, email: str, login: str, senha: str):
        super().__init__(matricula, nome, email, login, senha, self.LIMITE_LIVROS_PADRAO)