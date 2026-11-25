import os
import unittest
from src.application.services.facade_singleton_controller import FacadeSingletonController
from src.infrastructure.adapters.logger_adapter import PythonLoggerAdapter
from src.infrastructure.factories.repository_factory import (
    BinaryRepositoryFactory,
    MemoryRepositoryFactory,
)
from src.infrastructure.memory.livro_repository_memory import LivroRepositoryMemory
from src.infrastructure.memory.usuario_repository_memory import UsuarioRepositoryMemory


class TestSprint4Padroes(unittest.TestCase):
    ARQ_HTML = "test_relatorio.html"
    ARQ_TXT = "test_relatorio.txt"
    ARQ_BIN_USER = "test_s4_users.bin"
    ARQ_BIN_LIVRO = "test_s4_livros.bin"

    def setUp(self) -> None:
        FacadeSingletonController.reset_instance()
        factory = MemoryRepositoryFactory()
        self.facade = FacadeSingletonController.get_instance(
            factory.criar_usuario_repository(),
            factory.criar_livro_repository(),
        )

    def tearDown(self) -> None:
        FacadeSingletonController.reset_instance()
        for arquivo in (self.ARQ_HTML, self.ARQ_TXT, self.ARQ_BIN_USER, self.ARQ_BIN_LIVRO):
            if os.path.exists(arquivo):
                try:
                    os.remove(arquivo)
                except OSError:
                    pass

    def test_abstract_factory_cria_repositorios_corretos(self) -> None:
        mem_factory = MemoryRepositoryFactory()
        self.assertIsInstance(mem_factory.criar_usuario_repository(), UsuarioRepositoryMemory)
        self.assertIsInstance(mem_factory.criar_livro_repository(), LivroRepositoryMemory)

        bin_factory = BinaryRepositoryFactory(self.ARQ_BIN_USER, self.ARQ_BIN_LIVRO)
        user_repo = bin_factory.criar_usuario_repository()
        livro_repo = bin_factory.criar_livro_repository()
        self.assertIsNotNone(user_repo)
        self.assertIsNotNone(livro_repo)

    def test_adapter_logger_cria_arquivo_de_log(self) -> None:
        logger = PythonLoggerAdapter()
        logger.log_info("Teste automatizado do Adapter de Log")
        self.assertTrue(os.path.exists("sistema_biblioteca.log"))

    def test_template_method_gera_relatorio_html_e_txt(self) -> None:
        self.facade.cadastrar_usuario("aluno", "2026999", "Maria", "maria@ufpb.br", "marias", "SenhaForte@1")
        self.facade.cadastrar_livro("978-99", "Arquitetura Limpa", "Robert Martin", 2019)

        # Testar geração HTML
        conteudo_html = self.facade.exportar_relatorio_estatisticas("html", self.ARQ_HTML)
        self.assertTrue(os.path.exists(self.ARQ_HTML))
        self.assertIn("<html>", conteudo_html)
        self.assertIn("<b>Usuarios:</b> 1 cadastros ativos", conteudo_html)
        self.assertIn("<b>Livros:</b> 1 cadastros ativos", conteudo_html)

        # Testar geração TXT
        conteudo_txt = self.facade.exportar_relatorio_estatisticas("txt", self.ARQ_TXT)
        self.assertTrue(os.path.exists(self.ARQ_TXT))
        self.assertIn("RELATÓRIO DE ESTATÍSTICAS DO SISTEMA", conteudo_txt)
        self.assertIn("- Usuarios: 1 cadastros ativos", conteudo_txt)

    def test_template_method_rejeita_formato_invalido(self) -> None:
        with self.assertRaises(ValueError):
            self.facade.exportar_relatorio_estatisticas("pdf", "invalido.pdf")


if __name__ == "__main__":
    unittest.main()