from typing import Any, Dict, List, Optional
from src.application.commands.biblioteca_commands import (
    AtualizarLivroCommand,
    BuscarLivroPorIsbnCommand,
    BuscarUsuarioPorMatriculaCommand,
    CadastrarLivroCommand,
    CadastrarUsuarioCommand,
    DesfazerUltimaAtualizacaoLivroCommand,
    DevolverLivroCommand,
    EmprestarLivroCommand,
    ExportarRelatorioEstatisticasCommand,
    ListarLivrosCommand,
    ListarLivrosPorLocatarioCommand,
    ListarUsuariosCommand,
    ObterQuantidadeEntidadesCommand,
    RemoverLivroCommand,
)
from src.application.commands.command import CommandInvoker
from src.application.contracts.livro_repository import ILivroRepository
from src.application.contracts.usuario_repository import IUsuarioRepository
from src.application.memento.livro_memento import LivroCaretaker, LivroOriginator
from src.application.services.livro_service import LivroService
from src.application.services.usuario_service import UsuarioService
from src.domain.entities.livro import Livro
from src.domain.entities.usuario import Usuario
from src.infrastructure.adapters.logger_adapter import ILogger, PythonLoggerAdapter


class FacadeSingletonController:
    """Fachada única (Facade + Singleton) que orquestra operações via Command e Memento."""

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

        # Padrão Adapter (Logger) + Invoker (Command)
        self._logger: ILogger = PythonLoggerAdapter()
        self._invoker = CommandInvoker(self._logger)

        # Padrão Memento (Originator + Caretaker para Livro)
        self._livro_originator = LivroOriginator(self._livro_service)
        self._livro_caretaker = LivroCaretaker()

        self._logger.log_info("FacadeSingletonController inicializado com sucesso.")
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

    # --- Contagem de Entidades ---

    def obter_quantidade_entidades(self) -> Dict[str, int]:
        comando = ObterQuantidadeEntidadesCommand(self._usuario_service, self._livro_service)
        return self._invoker.executar(comando)

    # --- Operações de Usuários ---

    def cadastrar_usuario(
        self,
        tipo: str,
        matricula: str,
        nome: str,
        email: str,
        login: str,
        senha: str
    ) -> Usuario:
        comando = CadastrarUsuarioCommand(
            usuario_service=self._usuario_service,
            tipo=tipo,
            matricula=matricula,
            nome=nome,
            email=email,
            login=login,
            senha=senha
        )
        return self._invoker.executar(comando)

    def listar_usuarios(self) -> List[Usuario]:
        comando = ListarUsuariosCommand(self._usuario_service)
        return self._invoker.executar(comando)

    def buscar_usuario_por_matricula(self, matricula: str) -> Optional[Usuario]:
        comando = BuscarUsuarioPorMatriculaCommand(self._usuario_repo, matricula)
        return self._invoker.executar(comando)

    # --- Operações de Livros (CRUD + Empréstimo + Memento) ---

    def cadastrar_livro(self, isbn: str, titulo: str, autor: str, ano: int) -> Livro:
        comando = CadastrarLivroCommand(self._livro_service, isbn, titulo, autor, ano)
        return self._invoker.executar(comando)

    def buscar_livro_por_isbn(self, isbn: str) -> Livro:
        comando = BuscarLivroPorIsbnCommand(self._livro_service, isbn)
        return self._invoker.executar(comando)

    def listar_livros(self) -> List[Livro]:
        comando = ListarLivrosCommand(self._livro_service)
        return self._invoker.executar(comando)

    def listar_livros_por_locatario(self, matricula: str) -> List[Livro]:
        comando = ListarLivrosPorLocatarioCommand(self._livro_service, matricula)
        return self._invoker.executar(comando)

    def atualizar_livro(
        self,
        isbn: str,
        titulo: Optional[str] = None,
        autor: Optional[str] = None,
        ano: Optional[int] = None
    ) -> Livro:
        comando = AtualizarLivroCommand(
            livro_service=self._livro_service,
            originator=self._livro_originator,
            caretaker=self._livro_caretaker,
            isbn=isbn,
            titulo=titulo,
            autor=autor,
            ano=ano
        )
        return self._invoker.executar(comando)

    def desfazer_ultima_atualizacao_livro(self) -> Livro:
        comando = DesfazerUltimaAtualizacaoLivroCommand(
            originator=self._livro_originator,
            caretaker=self._livro_caretaker
        )
        return self._invoker.executar(comando)

    def remover_livro(self, isbn: str) -> bool:
        comando = RemoverLivroCommand(self._livro_service, isbn)
        return self._invoker.executar(comando)

    def emprestar_livro(self, isbn: str, matricula_usuario: str) -> Livro:
        comando = EmprestarLivroCommand(self._livro_service, isbn, matricula_usuario)
        return self._invoker.executar(comando)

    def devolver_livro(self, isbn: str) -> Livro:
        comando = DevolverLivroCommand(self._livro_service, isbn)
        return self._invoker.executar(comando)

    # --- Exportação de Relatórios (Template Method via Command) ---

    def exportar_relatorio_estatisticas(self, formato: str, caminho_arquivo: str) -> str:
        comando = ExportarRelatorioEstatisticasCommand(
            usuario_service=self._usuario_service,
            livro_service=self._livro_service,
            formato=formato,
            caminho_arquivo=caminho_arquivo
        )
        return self._invoker.executar(comando)