import sys
from src.application.services.usuario_service import UsuarioService
from src.domain.exceptions.usuario_exceptions import PersistenciaException
from src.infrastructure.binary.usuario_repository_binary import UsuarioRepositoryBinary
from src.infrastructure.memory.usuario_repository_memory import UsuarioRepositoryMemory
from src.presentation.cli import UserCLI


def selecionar_repositorio():
    print("=== CONFIGURAÇÃO DE PERSISTÊNCIA ===")
    print("1. Coleção em Memória RAM")
    print("2. Arquivo Binário (.bin)")
    
    while True:
        opcao = input("Selecione o mecanismo de armazenamento: ").strip()
        if opcao == "1":
            return UsuarioRepositoryMemory(), "Memória RAM"
        elif opcao == "2":
            try:
                return UsuarioRepositoryBinary("usuarios.bin"), "Arquivo Binário"
            except PersistenciaException as erro:
                print(f"Falha ao iniciar repositório binário: {erro}")
                sys.exit(1)
        else:
            print("Opção inválida. Digite 1 ou 2.")


def main() -> None:
    repositorio, nome_mecanismo = selecionar_repositorio()
    servico = UsuarioService(repositorio)
    cli = UserCLI(servico, nome_mecanismo)
    cli.executar()


if __name__ == "__main__":
    main()