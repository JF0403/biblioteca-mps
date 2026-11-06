import sys
from src.application.services.facade_singleton_controller import FacadeSingletonController
from src.domain.exceptions.usuario_exceptions import PersistenciaException
from src.infrastructure.binary.livro_repository_binary import LivroRepositoryBinary
from src.infrastructure.binary.usuario_repository_binary import UsuarioRepositoryBinary
from src.infrastructure.memory.livro_repository_memory import LivroRepositoryMemory
from src.infrastructure.memory.usuario_repository_memory import UsuarioRepositoryMemory
from src.presentation.cli import UserCLI


def inicializar_fachada():
    print("=== CONFIGURAÇÃO DE PERSISTÊNCIA ===")
    print("1. Coleção em Memória RAM")
    print("2. Arquivo Binário (.bin)")

    while True:
        opcao = input("Selecione o mecanismo de armazenamento: ").strip()
        if opcao == "1":
            user_repo = UsuarioRepositoryMemory()
            book_repo = LivroRepositoryMemory()
            facade = FacadeSingletonController(user_repo, book_repo)
            return facade, "Memória RAM"
        elif opcao == "2":
            try:
                user_repo = UsuarioRepositoryBinary("usuarios.bin")
                book_repo = LivroRepositoryBinary("livros.bin")
                facade = FacadeSingletonController(user_repo, book_repo)
                return facade, "Arquivo Binário"
            except PersistenciaException as erro:
                print(f"Falha ao iniciar repositórios binários: {erro}")
                sys.exit(1)
        else:
            print("Opção inválida. Digite 1 ou 2.")


def main() -> None:
    facade, nome_mecanismo = inicializar_fachada()
    cli = UserCLI(facade, nome_mecanismo)
    cli.executar()


if __name__ == "__main__":
    main()