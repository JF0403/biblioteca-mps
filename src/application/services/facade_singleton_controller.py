from typing import Any, Dict, List, Optional
from src.application.contracts.livro_repository import ILivroRepository
from src.application.contracts.usuario_repository import IUsuarioRepository
from src.application.services.livro_service import LivroService
from src.application.services.usuario_service import UsuarioService
from src.domain.entities.livro import Livro
from src.domain.entities.usuario import Usuario


class FacadeSingletonController:
    """Fachada única (Facade) com instância única (Singleton) para os Gerentes/Controllers."""

    _instancia: Optional["FacadeSingletonController"] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "FacadeSingletonController":
        if cls._instancia is None:
            cls._instancia = super(FacadeSingletonController, cls).__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(
        self,
        usuario_repository: Optional[IUsuarioRepository] = None,
        livro_repository: Optional[ILivroRepository] = None
    ) -> None:
        if getattr(self, "_inicializado", False):
            return

        if usuario_repository is None or livro_repository is None:
            raise ValueError("Os repositórios de usuário e livro são obrigatórios na primeira inicialização.")

        self._usuario_repo = usuario_repository
        self._livro_repo = livro_repository

        self._usuario_service = UsuarioService(self._usuario_repo)
        self._livro_service = LivroService(
            livro_repository=self._livro_repo,
            usuario_repository=self._usuario_repo
        )
        self._inicializado = True

    @classmethod
    def get_instance(
        cls,
        usuario_repository: Optional[IUsuarioRepository] = None,
        livro_repository: Optional[ILivroRepository] = None
    ) -> "FacadeSingletonController":
        """Método de acesso estático à instância Singleton."""
        if cls._instancia is None:
            if usuario_repository is None or livro_repository is None:
                raise ValueError("Instância ainda não criada. Forneça os repositórios.")
            cls._instancia = cls(usuario_repository, livro_repository)
        return cls._instancia

    @classmethod
    def reset_instance(cls) -> None:
        """Método utilitário para resetar a instância em baterias de testes."""
        cls._instancia = None

    # --- Método exigido pela Sprint 3: Quantidade de Entidades ---

    def obter_quantidade_entidades(self) -> Dict[str, int]:
        """Retorna a contagem das entidades cadastradas no sistema."""
        total_usuarios = len(self._usuario_service.listar_usuarios())
        total_livros = len(self._livro_service.listar_livros())
        return {
            "usuarios": total_usuarios,
            "livros": total_livros,
            "total": total_usuarios + total_livros
        }

    # --- Fachada para Operações de Usuários ---

    def cadastrar_usuario(
        self,
        tipo: str,
        matricula: str,
        nome: str,
        email: str,
        login: str,
        senha: str
    ) -> Usuario:
        return self._usuario_service.cadastrar_usuario(
            tipo=tipo,
            matricula=matricula,
            nome=nome,
            email=email,
            login=login,
            senha=senha
        )

    def listar_usuarios(self) -> List[Usuario]:
        return self._usuario_service.listar_usuarios()

    def buscar_usuario_por_matricula(self, matricula: str) -> Optional[Usuario]:
        return self._usuario_repo.buscar_por_matricula(matricula)

    # --- Fachada para Operações de Livros (CRUD Completo) ---

    def cadastrar_livro(self, isbn: str, titulo: str, autor: str, ano: int) -> Livro:
        return self._livro_service.cadastrar_livro(isbn, titulo, autor, ano)

    def buscar_livro_por_isbn(self, isbn: str) -> Livro:
        return self._livro_service.buscar_por_isbn(isbn)

    def listar_livros(self) -> List[Livro]:
        return self._livro_service.listar_livros()

    def listar_livros_por_locatario(self, matricula: str) -> List[Livro]:
        return self._livro_service.listar_livros_por_locatario(matricula)

    def atualizar_livro(
        self,
        isbn: str,
        titulo: Optional[str] = None,
        autor: Optional[str] = None,
        ano: Optional[int] = None
    ) -> Livro:
        return self._livro_service.atualizar_livro(isbn, titulo, autor, ano)

    def remover_livro(self, isbn: str) -> bool:
        return self._livro_service.remover_livro(isbn)

    def emprestar_livro(self, isbn: str, matricula_usuario: str) -> Livro:
        return self._livro_service.associar_locatario(isbn, matricula_usuario)

    def devolver_livro(self, isbn: str) -> Livro:
        return self._livro_service.desassociar_locatario(isbn)