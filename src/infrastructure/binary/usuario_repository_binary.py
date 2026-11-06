import os
import pickle
from typing import Dict, List, Optional
from src.application.contracts.usuario_repository import IUsuarioRepository
from src.domain.entities.usuario import Usuario
from src.domain.exceptions.usuario_exceptions import PersistenciaException


class UsuarioRepositoryBinary(IUsuarioRepository):
    """Implementação de persistência em arquivo binário com tratamento de exceções de I/O."""

    def __init__(self, caminho_arquivo: str = "usuarios.bin") -> None:
        self.caminho_arquivo = caminho_arquivo
        self._inicializar_arquivo()

    def _inicializar_arquivo(self) -> None:
        if not os.path.exists(self.caminho_arquivo):
            try:
                with open(self.caminho_arquivo, "wb") as f:
                    pickle.dump({}, f)
            except (IOError, OSError) as erro:
                raise PersistenciaException(f"Falha ao inicializar arquivo binário: {erro}")

    def _ler_dados(self) -> Dict[str, Usuario]:
        try:
            with open(self.caminho_arquivo, "rb") as f:
                return pickle.load(f)
        except EOFError:
            return {}
        except (IOError, OSError, pickle.PickleError) as erro:
            raise PersistenciaException(f"Falha ao ler dados do arquivo binário: {erro}")

    def _gravar_dados(self, dados: Dict[str, Usuario]) -> None:
        try:
            with open(self.caminho_arquivo, "wb") as f:
                pickle.dump(dados, f)
        except (IOError, OSError, pickle.PickleError) as erro:
            raise PersistenciaException(f"Falha ao persistir dados no arquivo binário: {erro}")

    def salvar(self, usuario: Usuario) -> None:
        dados = self._ler_dados()
        dados[usuario.matricula] = usuario
        self._gravar_dados(dados)

    def buscar_por_matricula(self, matricula: str) -> Optional[Usuario]:
        dados = self._ler_dados()
        return dados.get(matricula.strip())

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        dados = self._ler_dados()
        email_limpo = email.strip().lower()
        for usuario in dados.values():
            if usuario.email.lower() == email_limpo:
                return usuario
        return None

    def buscar_por_login(self, login: str) -> Optional[Usuario]:
        dados = self._ler_dados()
        login_limpo = login.strip().lower()
        for usuario in dados.values():
            if usuario.login.lower() == login_limpo:
                return usuario
        return None

    def listar_todos(self) -> List[Usuario]:
        dados = self._ler_dados()
        return list(dados.values())