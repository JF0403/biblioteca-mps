from typing import Dict, List, Optional
from src.application.commands.command import Command
from src.application.contracts.usuario_repository import IUsuarioRepository
from src.application.memento.livro_memento import LivroCaretaker, LivroOriginator
from src.application.services.livro_service import LivroService
from src.application.services.relatorio_template import (
    RelatorioEstatisticasHTML,
    RelatorioEstatisticasTXT,
)
from src.application.services.usuario_service import UsuarioService
from src.domain.entities.livro import Livro
from src.domain.entities.usuario import Usuario
from src.domain.exceptions.livro_exceptions import LivroInvalidoException


class ObterQuantidadeEntidadesCommand(Command):
    def __init__(self, usuario_service: UsuarioService, livro_service: LivroService) -> None:
        self._usuario_service = usuario_service
        self._livro_service = livro_service

    def execute(self) -> Dict[str, int]:
        total_usuarios = len(self._usuario_service.listar_usuarios())
        total_livros = len(self._livro_service.listar_livros())
        return {
            "usuarios": total_usuarios,
            "livros": total_livros,
            "total": total_usuarios + total_livros
        }


class CadastrarUsuarioCommand(Command):
    def __init__(
        self,
        usuario_service: UsuarioService,
        tipo: str,
        matricula: str,
        nome: str,
        email: str,
        login: str,
        senha: str
    ) -> None:
        self._usuario_service = usuario_service
        self._tipo = tipo
        self._matricula = matricula
        self._nome = nome
        self._email = email
        self._login = login
        self._senha = senha

    def execute(self) -> Usuario:
        return self._usuario_service.cadastrar_usuario(
            tipo=self._tipo,
            matricula=self._matricula,
            nome=self._nome,
            email=self._email,
            login=self._login,
            senha=self._senha
        )


class ListarUsuariosCommand(Command):
    def __init__(self, usuario_service: UsuarioService) -> None:
        self._usuario_service = usuario_service

    def execute(self) -> List[Usuario]:
        return self._usuario_service.listar_usuarios()


class BuscarUsuarioPorMatriculaCommand(Command):
    def __init__(self, usuario_repo: IUsuarioRepository, matricula: str) -> None:
        self._usuario_repo = usuario_repo
        self._matricula = matricula

    def execute(self) -> Optional[Usuario]:
        return self._usuario_repo.buscar_por_matricula(self._matricula)


class CadastrarLivroCommand(Command):
    def __init__(self, livro_service: LivroService, isbn: str, titulo: str, autor: str, ano: int) -> None:
        self._livro_service = livro_service
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor
        self._ano = ano

    def execute(self) -> Livro:
        return self._livro_service.cadastrar_livro(self._isbn, self._titulo, self._autor, self._ano)


class BuscarLivroPorIsbnCommand(Command):
    def __init__(self, livro_service: LivroService, isbn: str) -> None:
        self._livro_service = livro_service
        self._isbn = isbn

    def execute(self) -> Livro:
        return self._livro_service.buscar_por_isbn(self._isbn)


class ListarLivrosCommand(Command):
    def __init__(self, livro_service: LivroService) -> None:
        self._livro_service = livro_service

    def execute(self) -> List[Livro]:
        return self._livro_service.listar_livros()


class ListarLivrosPorLocatarioCommand(Command):
    def __init__(self, livro_service: LivroService, matricula: str) -> None:
        self._livro_service = livro_service
        self._matricula = matricula

    def execute(self) -> List[Livro]:
        return self._livro_service.listar_livros_por_locatario(self._matricula)


class AtualizarLivroCommand(Command):
    """Atualiza um livro salvando o estado anterior no Caretaker (Memento)."""

    def __init__(
        self,
        livro_service: LivroService,
        originator: LivroOriginator,
        caretaker: LivroCaretaker,
        isbn: str,
        titulo: Optional[str] = None,
        autor: Optional[str] = None,
        ano: Optional[int] = None
    ) -> None:
        self._livro_service = livro_service
        self._originator = originator
        self._caretaker = caretaker
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor
        self._ano = ano

    def execute(self) -> Livro:
        snapshot_anterior = self._originator.criar_memento(self._isbn)
        livro_atualizado = self._livro_service.atualizar_livro(
            self._isbn,
            self._titulo,
            self._autor,
            self._ano
        )
        self._caretaker.salvar(snapshot_anterior)
        return livro_atualizado


class DesfazerUltimaAtualizacaoLivroCommand(Command):
    """Restaura a última atualização realizada na entidade Livro usando Memento."""

    def __init__(self, originator: LivroOriginator, caretaker: LivroCaretaker) -> None:
        self._originator = originator
        self._caretaker = caretaker

    def execute(self) -> Livro:
        memento = self._caretaker.obter_ultimo()
        if memento is None:
            raise LivroInvalidoException("Não há nenhuma atualização de livro para desfazer.")

        livro_restaurado = self._originator.restaurar_memento(memento)
        self._caretaker.limpar()
        return livro_restaurado


class RemoverLivroCommand(Command):
    def __init__(self, livro_service: LivroService, isbn: str) -> None:
        self._livro_service = livro_service
        self._isbn = isbn

    def execute(self) -> bool:
        return self._livro_service.remover_livro(self._isbn)


class EmprestarLivroCommand(Command):
    def __init__(self, livro_service: LivroService, isbn: str, matricula_usuario: str) -> None:
        self._livro_service = livro_service
        self._isbn = isbn
        self._matricula_usuario = matricula_usuario

    def execute(self) -> Livro:
        return self._livro_service.associar_locatario(self._isbn, self._matricula_usuario)


class DevolverLivroCommand(Command):
    def __init__(self, livro_service: LivroService, isbn: str) -> None:
        self._livro_service = livro_service
        self._isbn = isbn

    def execute(self) -> Livro:
        return self._livro_service.desassociar_locatario(self._isbn)


class ExportarRelatorioEstatisticasCommand(Command):
    def __init__(
        self,
        usuario_service: UsuarioService,
        livro_service: LivroService,
        formato: str,
        caminho_arquivo: str
    ) -> None:
        self._usuario_service = usuario_service
        self._livro_service = livro_service
        self._formato = formato
        self._caminho_arquivo = caminho_arquivo

    def execute(self) -> str:
        estatisticas = ObterQuantidadeEntidadesCommand(
            self._usuario_service,
            self._livro_service
        ).execute()

        if self._formato.lower() == "html":
            gerador = RelatorioEstatisticasHTML()
        elif self._formato.lower() == "txt":
            gerador = RelatorioEstatisticasTXT()
        else:
            raise ValueError("Formato de relatório não suportado. Use 'html' ou 'txt'.")

        return gerador.gerar_relatorio(estatisticas, self._caminho_arquivo)