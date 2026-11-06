from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.usuario import Usuario


class IUsuarioRepository(ABC):
    """Interface abstrata de persistencia de usuarios."""

    @abstractmethod
    def salvar(self, usuario: Usuario) -> None:
        """Persiste um usuario na colecao."""
        pass

    @abstractmethod
    def buscar_por_matricula(self, matricula: str) -> Optional[Usuario]:
        """Busca um usuario pela matricula."""
        pass

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca um usuario pelo email."""
        pass

    @abstractmethod
    def listar_todos(self) -> List[Usuario]:
        """Retorna todos os usuarios armazenados."""
        pass