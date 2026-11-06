from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.usuario import Usuario


class IUsuarioRepository(ABC):
    """Interface abstrata de persistência de usuários."""

    @abstractmethod
    def salvar(self, usuario: Usuario) -> None:
        """Persiste um usuário na coleção."""
        pass

    @abstractmethod
    def buscar_por_matricula(self, matricula: str) -> Optional[Usuario]:
        """Busca um usuário pela matrícula."""
        pass

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca um usuário pelo e-mail."""
        pass

    @abstractmethod
    def buscar_por_login(self, login: str) -> Optional[Usuario]:
        """Busca um usuário pelo login."""
        pass

    @abstractmethod
    def listar_todos(self) -> List[Usuario]:
        """Retorna todos os usuários armazenados."""
        pass