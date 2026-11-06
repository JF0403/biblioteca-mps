from typing import List, Optional
from src.application.contracts.livro_repository import ILivroRepository
from src.application.contracts.usuario_repository import IUsuarioRepository
from src.domain.entities.livro import Livro
from src.domain.exceptions.livro_exceptions import (
    LivroDuplicadoException,
    LivroInvalidoException,
    LivroNaoEncontradoException,
)
from src.domain.exceptions.usuario_exceptions import DadosUsuarioInvalidosException


class LivroService:
    """Gerente (Controller) responsável pelas regras de negócio e CRUD de Livros."""

    def __init__(
        self,
        livro_repository: ILivroRepository,
        usuario_repository: Optional[IUsuarioRepository] = None
    ) -> None:
        self._livro_repo = livro_repository
        self._usuario_repo = usuario_repository

    def cadastrar_livro(self, isbn: str, titulo: str, autor: str, ano: int) -> Livro:
        isbn_limpo = isbn.strip() if isbn else ""
        if self._livro_repo.buscar_por_isbn(isbn_limpo):
            raise LivroDuplicadoException(f"Já existe um livro cadastrado com o ISBN '{isbn_limpo}'.")

        livro = Livro(isbn=isbn_limpo, titulo=titulo, autor=autor, ano=ano)
        self._livro_repo.salvar(livro)
        return livro

    def buscar_por_isbn(self, isbn: str) -> Livro:
        isbn_limpo = isbn.strip() if isbn else ""
        livro = self._livro_repo.buscar_por_isbn(isbn_limpo)
        if not livro:
            raise LivroNaoEncontradoException(f"Nenhum livro encontrado com o ISBN '{isbn_limpo}'.")
        return livro

    def listar_livros(self) -> List[Livro]:
        return self._livro_repo.listar_todos()

    def listar_livros_por_locatario(self, matricula: str) -> List[Livro]:
        return self._livro_repo.listar_por_locatario(matricula)

    def atualizar_livro(
        self,
        isbn: str,
        titulo: Optional[str] = None,
        autor: Optional[str] = None,
        ano: Optional[int] = None
    ) -> Livro:
        livro = self.buscar_por_isbn(isbn)

        if titulo is not None:
            if not titulo.strip():
                raise LivroInvalidoException("O título atualizado não pode ser vazio.")
            livro.titulo = titulo.strip()

        if autor is not None:
            if not autor.strip():
                raise LivroInvalidoException("O autor atualizado não pode ser vazio.")
            livro.autor = autor.strip()

        if ano is not None:
            try:
                ano_int = int(ano)
                if ano_int <= 0 or ano_int > 2100:
                    raise LivroInvalidoException("Ano atualizado inválido.")
                livro.ano = ano_int
            except (ValueError, TypeError):
                raise LivroInvalidoException("O ano deve ser um valor numérico inteiro.")

        self._livro_repo.salvar(livro)
        return livro

    def associar_locatario(self, isbn: str, matricula: str) -> Livro:
        livro = self.buscar_por_isbn(isbn)
        if livro.esta_emprestado:
            raise LivroInvalidoException(
                f"O livro '{livro.titulo}' já está emprestado ao usuário matrícula '{livro.matricula_locatario}'."
            )

        matricula_limpa = matricula.strip() if matricula else ""
        if self._usuario_repo is not None:
            usuario = self._usuario_repo.buscar_por_matricula(matricula_limpa)
            if not usuario:
                raise DadosUsuarioInvalidosException(
                    f"Usuário com matrícula '{matricula_limpa}' não encontrado."
                )

        livro.associar_locatario(matricula_limpa)
        self._livro_repo.salvar(livro)
        return livro

    def desassociar_locatario(self, isbn: str) -> Livro:
        livro = self.buscar_por_isbn(isbn)
        if not livro.esta_emprestado:
            raise LivroInvalidoException(f"O livro '{livro.titulo}' não se encontra emprestado.")

        livro.desassociar_locatario()
        self._livro_repo.salvar(livro)
        return livro

    def remover_livro(self, isbn: str) -> bool:
        livro = self.buscar_por_isbn(isbn)
        if livro.esta_emprestado:
            raise LivroInvalidoException(
                f"Não é possível remover o livro '{livro.titulo}' porque ele está emprestado no momento."
            )
        return self._livro_repo.remover(livro.isbn)