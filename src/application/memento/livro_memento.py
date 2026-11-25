from typing import Optional
from src.application.services.livro_service import LivroService
from src.domain.entities.livro import Livro


class LivroMemento:
    """Memento: armazena um snapshot imutável do estado de um Livro."""

    def __init__(self, isbn: str, titulo: str, autor: str, ano: int) -> None:
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor
        self._ano = ano

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def autor(self) -> str:
        return self._autor

    @property
    def ano(self) -> int:
        return self._ano


class LivroOriginator:
    """Originator: cria e restaura snapshots da entidade Livro via LivroService."""

    def __init__(self, livro_service: LivroService) -> None:
        self._livro_service = livro_service

    def criar_memento(self, isbn: str) -> LivroMemento:
        livro = self._livro_service.buscar_por_isbn(isbn)
        return LivroMemento(
            isbn=livro.isbn,
            titulo=livro.titulo,
            autor=livro.autor,
            ano=livro.ano
        )

    def restaurar_memento(self, memento: LivroMemento) -> Livro:
        return self._livro_service.atualizar_livro(
            memento.isbn,
            memento.titulo,
            memento.autor,
            memento.ano
        )


class LivroCaretaker:
    """Caretaker (Zelador): mantém apenas o memento da última atualização de Livro."""

    def __init__(self) -> None:
        self._ultimo_memento: Optional[LivroMemento] = None

    def salvar(self, memento: LivroMemento) -> None:
        self._ultimo_memento = memento

    def obter_ultimo(self) -> Optional[LivroMemento]:
        return self._ultimo_memento

    def tem_memento(self) -> bool:
        return self._ultimo_memento is not None

    def limpar(self) -> None:
        self._ultimo_memento = None