from typing import List
from src.application.contracts.usuario_repository import IUsuarioRepository
from src.domain.entities.usuario import Aluno, Professor, Usuario
from src.domain.exceptions.usuario_exceptions import (
    DadosUsuarioInvalidosException,
    UsuarioDuplicadoException,
)


class UsuarioService:
    def __init__(self, repositorio: IUsuarioRepository) -> None:
        self._repositorio = repositorio

    def cadastrar_usuario(
        self,
        tipo: str,
        matricula: str,
        nome: str,
        email: str,
        login: str,
        senha: str
    ) -> Usuario:
        matricula_limpa = matricula.strip() if matricula else ""
        email_limpo = email.strip().lower() if email else ""
        login_limpo = login.strip().lower() if login else ""

        if self._repositorio.buscar_por_matricula(matricula_limpa):
            raise UsuarioDuplicadoException(f"Matrícula '{matricula_limpa}' já cadastrada.")

        if self._repositorio.buscar_por_email(email_limpo):
            raise UsuarioDuplicadoException(f"E-mail '{email_limpo}' já cadastrado.")

        if self._repositorio.buscar_por_login(login_limpo):
            raise UsuarioDuplicadoException(f"Login '{login_limpo}' já cadastrado.")

        tipo_normalizado = tipo.strip().lower() if tipo else ""

        if tipo_normalizado == "aluno":
            usuario = Aluno(
                matricula=matricula_limpa,
                nome=nome,
                email=email_limpo,
                login=login,
                senha=senha
            )
        elif tipo_normalizado == "professor":
            usuario = Professor(
                matricula=matricula_limpa,
                nome=nome,
                email=email_limpo,
                login=login,
                senha=senha
            )
        else:
            raise DadosUsuarioInvalidosException("Tipo de usuário inválido. Escolha 'aluno' ou 'professor'.")

        self._repositorio.salvar(usuario)
        return usuario

    def listar_usuarios(self) -> List[Usuario]:
        return self._repositorio.listar_todos()