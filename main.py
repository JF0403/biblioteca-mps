import sys
from src.application.services.facade_singleton_controller import FacadeSingletonController
from src.domain.exceptions.usuario_exceptions import PersistenciaException
from src.infrastructure.factories.repository_factory import BinaryRepositoryFactory, MemoryRepositoryFactory
from src.presentation.cli import UserCLI


def inicializar_fachada():
    print("=== CONFIGURAÇÃO DE PERSISTÊNCIA ===")
    print("1. Coleção em Memória RAM")
    print("2. Arquivo Binário (.bin)")

    while True:
        opcao = input("Selecione o mecanismo de armazenamento: ").strip()
        if opcao == "1":
            factory = MemoryRepositoryFactory()
            usuario_repo = factory.criar_usuario_repository()
            livro_repo = factory.criar_livro_repository()
            facade = FacadeSingletonController.get_instance(usuario_repo, livro_repo)
            return facade, "Memória RAM"
        elif opcao == "2":
            try:
                factory = BinaryRepositoryFactory()
                usuario_repo = factory.criar_usuario_repository()
                livro_repo = factory.criar_livro_repository()
                facade = FacadeSingletonController.get_instance(usuario_repo, livro_repo)
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