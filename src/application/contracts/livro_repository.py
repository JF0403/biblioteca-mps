from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.livro import Livro


class ILivroRepository(ABC):
    """Interface abstrata para persistência de livros (CRUD completo)."""

    @abstractmethod
    def salvar(self, livro: Livro) -> None:
        """Cadastra ou atualiza um livro."""
        pass

    @abstractmethod
    def buscar_por_isbn(self, isbn: str) -> Optional[Livro]:
        """Busca um livro pelo ISBN único."""
        pass

    @abstractmethod
    def remover(self, isbn: str) -> bool:
        """Remove um livro pelo ISBN. Retorna True se removido, False caso contrário."""
        pass

    @abstractmethod
    def listar_todos(self) -> List[Livro]:
        """Retorna todos os livros cadastrados."""
        pass

    @abstractmethod
    def listar_por_locatario(self, matricula: str) -> List[Livro]:
        """Retorna todos os livros associados a uma matrícula de usuário."""
        pass