import unittest
from src.application.services.facade_singleton_controller import FacadeSingletonController
from src.domain.exceptions.livro_exceptions import (
    LivroDuplicadoException,
    LivroInvalidoException,
    LivroNaoEncontradoException,
)
from src.infrastructure.memory.livro_repository_memory import LivroRepositoryMemory
from src.infrastructure.memory.usuario_repository_memory import UsuarioRepositoryMemory


class TestFacadeSingletonController(unittest.TestCase):
    def setUp(self) -> None:
        FacadeSingletonController.reset_instance()
        self.usuario_repo = UsuarioRepositoryMemory()
        self.livro_repo = LivroRepositoryMemory()
        self.facade = FacadeSingletonController(self.usuario_repo, self.livro_repo)

    def tearDown(self) -> None:
        FacadeSingletonController.reset_instance()

    def test_deve_garantir_padrao_singleton(self) -> None:
        outra_facade = FacadeSingletonController()
        terceira_facade = FacadeSingletonController.get_instance()
        self.assertIs(self.facade, outra_facade)
        self.assertIs(self.facade, terceira_facade)

    def test_deve_retornar_quantidade_de_entidades_cadastradas(self) -> None:
        qtd_inicial = self.facade.obter_quantidade_entidades()
        self.assertEqual(qtd_inicial["usuarios"], 0)
        self.assertEqual(qtd_inicial["livros"], 0)
        self.assertEqual(qtd_inicial["total"], 0)

        self.facade.cadastrar_usuario(
            tipo="aluno",
            matricula="2026100",
            nome="Joao",
            email="joao@ufpb.br",
            login="joaof",
            senha="Password@123"
        )
        self.facade.cadastrar_livro(
            isbn="978-0132350884",
            titulo="Clean Code",
            autor="Robert C. Martin",
            ano=2008
        )

        qtd_atualizada = self.facade.obter_quantidade_entidades()
        self.assertEqual(qtd_atualizada["usuarios"], 1)
        self.assertEqual(qtd_atualizada["livros"], 1)
        self.assertEqual(qtd_atualizada["total"], 2)

    def test_crud_completo_livro_com_sucesso(self) -> None:
        # Create
        livro = self.facade.cadastrar_livro(
            isbn="978-0201616224",
            titulo="The Pragmatic Programmer",
            autor="Andy Hunt",
            ano=1999
        )
        self.assertEqual(livro.titulo, "The Pragmatic Programmer")

        # Read
        encontrado = self.facade.buscar_livro_por_isbn("978-0201616224")
        self.assertEqual(encontrado.autor, "Andy Hunt")
        self.assertEqual(len(self.facade.listar_livros()), 1)

        # Update
        atualizado = self.facade.atualizar_livro(
            isbn="978-0201616224",
            titulo="The Pragmatic Programmer - 20th Anniversary Edition",
            ano=2019
        )
        self.assertEqual(atualizado.titulo, "The Pragmatic Programmer - 20th Anniversary Edition")
        self.assertEqual(atualizado.ano, 2019)

        # Delete
        removido = self.facade.remover_livro("978-0201616224")
        self.assertTrue(removido)
        self.assertEqual(len(self.facade.listar_livros()), 0)

    def test_deve_lancar_excecao_para_isbn_duplicado(self) -> None:
        self.facade.cadastrar_livro("123", "Livro A", "Autor A", 2020)
        with self.assertRaises(LivroDuplicadoException):
            self.facade.cadastrar_livro("123", "Livro B", "Autor B", 2021)

    def test_deve_lancar_excecao_para_livro_inexistente(self) -> None:
        with self.assertRaises(LivroNaoEncontradoException):
            self.facade.buscar_livro_por_isbn("999999")

    def test_deve_lancar_excecao_ao_remover_livro_emprestado(self) -> None:
        self.facade.cadastrar_usuario(
            "aluno", "MAT01", "Aluno Teste", "teste@ufpb.br", "alunoteste", "Strong#2026"
        )
        self.facade.cadastrar_livro("456", "Refactoring", "Martin Fowler", 2018)
        self.facade.emprestar_livro("456", "MAT01")

        with self.assertRaises(LivroInvalidoException):
            self.facade.remover_livro("456")


if __name__ == "__main__":
    unittest.main()