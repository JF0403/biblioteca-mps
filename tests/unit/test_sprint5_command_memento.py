import os
import unittest
from src.application.commands.biblioteca_commands import CadastrarLivroCommand
from src.application.commands.command import CommandInvoker
from src.application.services.facade_singleton_controller import FacadeSingletonController
from src.application.services.livro_service import LivroService
from src.domain.exceptions.livro_exceptions import LivroInvalidoException
from src.infrastructure.factories.repository_factory import (
    BinaryRepositoryFactory,
    MemoryRepositoryFactory,
)


class TestSprint5CommandMemento(unittest.TestCase):
    ARQ_BIN_USER = "test_s5_users.bin"
    ARQ_BIN_LIVRO = "test_s5_livros.bin"

    def setUp(self) -> None:
        FacadeSingletonController.reset_instance()
        factory = MemoryRepositoryFactory()
        self.facade = FacadeSingletonController.get_instance(
            factory.criar_usuario_repository(),
            factory.criar_livro_repository()
        )

    def tearDown(self) -> None:
        FacadeSingletonController.reset_instance()
        for arquivo in (self.ARQ_BIN_USER, self.ARQ_BIN_LIVRO):
            if os.path.exists(arquivo):
                try:
                    os.remove(arquivo)
                except OSError:
                    pass

    def test_command_invoker_executa_comando_concreto(self) -> None:
        factory = MemoryRepositoryFactory()
        livro_service = LivroService(
            livro_repository=factory.criar_livro_repository(),
            usuario_repository=factory.criar_usuario_repository()
        )
        invoker = CommandInvoker()
        comando = CadastrarLivroCommand(livro_service, "CMD-01", "Design Patterns", "GoF", 1994)

        livro = invoker.executar(comando)
        self.assertEqual(livro.isbn, "CMD-01")
        self.assertEqual(livro.titulo, "Design Patterns")

    def test_memento_desfaz_ultima_atualizacao_de_livro(self) -> None:
        self.facade.cadastrar_livro("MEM-01", "Clean Code", "Robert C. Martin", 2008)
        self.facade.atualizar_livro("MEM-01", titulo="Clean Code 2nd Ed", autor="Uncle Bob", ano=2025)

        atualizado = self.facade.buscar_livro_por_isbn("MEM-01")
        self.assertEqual(atualizado.titulo, "Clean Code 2nd Ed")
        self.assertEqual(atualizado.ano, 2025)

        restaurado = self.facade.desfazer_ultima_atualizacao_livro()
        self.assertEqual(restaurado.titulo, "Clean Code")
        self.assertEqual(restaurado.autor, "Robert C. Martin")
        self.assertEqual(restaurado.ano, 2008)

    def test_memento_desfaz_apenas_a_ultima_atualizacao(self) -> None:
        self.facade.cadastrar_livro("MEM-02", "Versao 1", "Autor 1", 2020)
        self.facade.atualizar_livro("MEM-02", titulo="Versao 2", ano=2021)
        self.facade.atualizar_livro("MEM-02", titulo="Versao 3", ano=2022)

        # Desfaz apenas a última atualização (Versao 3 -> Versao 2)
        restaurado = self.facade.desfazer_ultima_atualizacao_livro()
        self.assertEqual(restaurado.titulo, "Versao 2")
        self.assertEqual(restaurado.ano, 2021)

        # Segunda tentativa de desfazer deve lançar exceção
        with self.assertRaises(LivroInvalidoException):
            self.facade.desfazer_ultima_atualizacao_livro()

    def test_memento_lanca_excecao_sem_atualizacao_previa(self) -> None:
        self.facade.cadastrar_livro("MEM-03", "Refactoring", "Martin Fowler", 2018)
        with self.assertRaises(LivroInvalidoException):
            self.facade.desfazer_ultima_atualizacao_livro()

    def test_memento_preserva_snapshot_se_atualizacao_falhar(self) -> None:
        self.facade.cadastrar_livro("MEM-04", "Original", "Autor", 2015)
        self.facade.atualizar_livro("MEM-04", titulo="Editado", ano=2020)

        # Atualização inválida não deve sobrescrever o memento válido anterior
        with self.assertRaises(LivroInvalidoException):
            self.facade.atualizar_livro("MEM-04", ano=3000)

        restaurado = self.facade.desfazer_ultima_atualizacao_livro()
        self.assertEqual(restaurado.titulo, "Original")
        self.assertEqual(restaurado.ano, 2015)

    def test_memento_persiste_restauracao_em_arquivo_binario(self) -> None:
        FacadeSingletonController.reset_instance()
        bin_factory = BinaryRepositoryFactory(self.ARQ_BIN_USER, self.ARQ_BIN_LIVRO)
        facade_bin = FacadeSingletonController.get_instance(
            bin_factory.criar_usuario_repository(),
            bin_factory.criar_livro_repository()
        )

        facade_bin.cadastrar_livro("BIN-MEM", "Titulo Original", "Autor Original", 2019)
        facade_bin.atualizar_livro("BIN-MEM", titulo="Titulo Errado", ano=2024)
        facade_bin.desfazer_ultima_atualizacao_livro()

        # Reabrir a partir do disco para confirmar persistência da restauração
        FacadeSingletonController.reset_instance()
        bin_factory_reaberto = BinaryRepositoryFactory(self.ARQ_BIN_USER, self.ARQ_BIN_LIVRO)
        facade_reaberta = FacadeSingletonController.get_instance(
            bin_factory_reaberto.criar_usuario_repository(),
            bin_factory_reaberto.criar_livro_repository()
        )

        livro = facade_reaberta.buscar_livro_por_isbn("BIN-MEM")
        self.assertEqual(livro.titulo, "Titulo Original")
        self.assertEqual(livro.ano, 2019)


if __name__ == "__main__":
    unittest.main()