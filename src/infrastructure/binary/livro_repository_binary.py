import os
import pickle
from typing import Dict, List, Optional
from src.application.contracts.livro_repository import ILivroRepository
from src.domain.entities.livro import Livro
from src.domain.exceptions.usuario_exceptions import PersistenciaException


class LivroRepositoryBinary(ILivroRepository):
    """Implementação de persistência de livros em arquivo binário com tratamento de I/O."""

    def __init__(self, caminho_arquivo: str = "livros.bin") -> None:
        self.caminho_arquivo = caminho_arquivo
        self._inicializar_arquivo()

    def _inicializar_arquivo(self) -> None:
        if not os.path.exists(self.caminho_arquivo):
            try:
                with open(self.caminho_arquivo, "wb") as f:
                    pickle.dump({}, f)
            except (IOError, OSError) as erro:
                raise PersistenciaException(f"Falha ao inicializar arquivo binário de livros: {erro}")

    def _ler_dados(self) -> Dict[str, Livro]:
        try:
            with open(self.caminho_arquivo, "rb") as f:
                return pickle.load(f)
        except EOFError:
            return {}
        except (IOError, OSError, pickle.PickleError) as erro:
            raise PersistenciaException(f"Falha ao ler dados de livros no arquivo binário: {erro}")

    def _gravar_dados(self, dados: Dict[str, Livro]) -> None:
        try:
            with open(self.caminho_arquivo, "wb") as f:
                pickle.dump(dados, f)
        except (IOError, OSError, pickle.PickleError) as erro:
            raise PersistenciaException(f"Falha ao gravar livros no arquivo binário: {erro}")

    def salvar(self, livro: Livro) -> None:
        dados = self._ler_dados()
        dados[livro.isbn] = livro
        self._gravar_dados(dados)

    def buscar_por_isbn(self, isbn: str) -> Optional[Livro]:
        dados = self._ler_dados()
        return dados.get(isbn.strip())

    def remover(self, isbn: str) -> bool:
        dados = self._ler_dados()
        isbn_limpo = isbn.strip()
        if isbn_limpo in dados:
            del dados[isbn_limpo]
            self._gravar_dados(dados)
            return True
        return False

    def listar_todos(self) -> List[Livro]:
        dados = self._ler_dados()
        return list(dados.values())

    def listar_por_locatario(self, matricula: str) -> List[Livro]:
        dados = self._ler_dados()
        matricula_limpa = matricula.strip()
        return [
            livro for livro in dados.values()
            if livro.matricula_locatario == matricula_limpa
        ]