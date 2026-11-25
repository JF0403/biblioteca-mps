from abc import ABC, abstractmethod
from src.application.contracts.usuario_repository import IUsuarioRepository
from src.application.contracts.livro_repository import ILivroRepository
from src.infrastructure.memory.usuario_repository_memory import UsuarioRepositoryMemory
from src.infrastructure.memory.livro_repository_memory import LivroRepositoryMemory
from src.infrastructure.binary.usuario_repository_binary import UsuarioRepositoryBinary
from src.infrastructure.binary.livro_repository_binary import LivroRepositoryBinary

class RepositoryFactory(ABC):
    """Abstract Factory para criação de repositórios."""
    
    @abstractmethod
    def criar_usuario_repository(self) -> IUsuarioRepository:
        pass

    @abstractmethod
    def criar_livro_repository(self) -> ILivroRepository:
        pass

class MemoryRepositoryFactory(RepositoryFactory):
    def criar_usuario_repository(self) -> IUsuarioRepository:
        return UsuarioRepositoryMemory()

    def criar_livro_repository(self) -> ILivroRepository:
        return LivroRepositoryMemory()

class BinaryRepositoryFactory(RepositoryFactory):
    def __init__(self, arquivo_usuarios="usuarios.bin", arquivo_livros="livros.bin"):
        self.arquivo_usuarios = arquivo_usuarios
        self.arquivo_livros = arquivo_livros

    def criar_usuario_repository(self) -> IUsuarioRepository:
        return UsuarioRepositoryBinary(self.arquivo_usuarios)

    def criar_livro_repository(self) -> ILivroRepository:
        return LivroRepositoryBinary(self.arquivo_livros)