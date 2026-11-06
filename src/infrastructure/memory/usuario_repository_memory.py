from typing import Dict, List, Optional
from src.application.contracts.usuario_repository import IUsuarioRepository
from src.domain.entities.usuario import Usuario


class UsuarioRepositoryMemory(IUsuarioRepository):
    """Implementacao de repositorio desacoplado utilizando dicionario/colecao em memoria RAM."""

    def __init__(self) -> None:
        self._usuarios: Dict[str, Usuario] = {}

    def salvar(self, usuario: Usuario) -> None:
        self._usuarios[usuario.matricula] = usuario

    def buscar_por_matricula(self, matricula: str) -> Optional[Usuario]:
        return self._usuarios.get(matricula.strip())

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        email_limpo = email.strip().lower()
        for usuario in self._usuarios.values():
            if usuario.email.lower() == email_limpo:
                return usuario
        return None

    def listar_todos(self) -> List[Usuario]:
        return list(self._usuarios.values())