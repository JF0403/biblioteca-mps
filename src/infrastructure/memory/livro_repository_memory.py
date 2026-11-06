from typing import Dict, List, Optional
from src.application.contracts.livro_repository import ILivroRepository
from src.domain.entities.livro import Livro


class LivroRepositoryMemory(ILivroRepository):
    """Implementação em memória RAM para armazenamento de livros."""

    def __init__(self) -> None:
        self._livros: Dict[str, Livro] = {}

    def salvar(self, livro: Livro) -> None:
        self._livros[livro.isbn] = livro

    def buscar_por_isbn(self, isbn: str) -> Optional[Livro]:
        return self._livros.get(isbn.strip())

    def remover(self, isbn: str) -> bool:
        isbn_limpo = isbn.strip()
        if isbn_limpo in self._livros:
            del self._livros[isbn_limpo]
            return True
        return False

    def listar_todos(self) -> List[Livro]:
        return list(self._livros.values())

    def listar_por_locatario(self, matricula: str) -> List[Livro]:
        matricula_limpa = matricula.strip()
        return [
            livro for livro in self._livros.values()
            if livro.matricula_locatario == matricula_limpa
        ]