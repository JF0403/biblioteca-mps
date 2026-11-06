from src.application.services.usuario_service import UsuarioService
from src.infrastructure.memory.usuario_repository_memory import UsuarioRepositoryMemory
from src.presentation.cli import UserCLI


def main() -> None:
    repositorio_ram = UsuarioRepositoryMemory()
    servico = UsuarioService(repositorio_ram)
    cli = UserCLI(servico)
    cli.executar()


if __name__ == "__main__":
    main()