import os
import unittest
from src.application.services.facade_singleton_controller import FacadeSingletonController
from src.domain.exceptions.livro_exceptions import (
    LivroDuplicadoException,
    LivroInvalidoException,
    LivroNaoEncontradoException,
)
from src.domain.exceptions.usuario_exceptions import (
    DadosUsuarioInvalidosException,
    LoginInvalidoException,
)
from src.infrastructure.binary.livro_repository_binary import LivroRepositoryBinary
from src.infrastructure.binary.usuario_repository_binary import UsuarioRepositoryBinary
from src.infrastructure.memory.livro_repository_memory import LivroRepositoryMemory
from src.infrastructure.memory.usuario_repository_memory import UsuarioRepositoryMemory


class TestFacadeSingletonController(unittest.TestCase):
    ARQUIVO_USUARIOS_TESTE = "test_usuarios_facade.bin"
    ARQUIVO_LIVROS_TESTE = "test_livros_facade.bin"

    def setUp(self) -> None:
        FacadeSingletonController.reset_instance()
        self.usuario_repo = UsuarioRepositoryMemory()
        self.livro_repo = LivroRepositoryMemory()
        self.facade = FacadeSingletonController(self.usuario_repo, self.livro_repo)

    def tearDown(self) -> None:
        FacadeSingletonController.reset_instance()
        for caminho in (self.ARQUIVO_USUARIOS_TESTE, self.ARQUIVO_LIVROS_TESTE):
            if os.path.exists(caminho):
                try:
                    os.remove(caminho)
                except OSError:
                    pass

    # 1. Padrão Singleton
    def test_deve_garantir_padrao_singleton(self) -> None:
        outra_facade = FacadeSingletonController()
        terceira_facade = FacadeSingletonController.get_instance()
        self.assertIs(self.facade, outra_facade)
        self.assertIs(self.facade, terceira_facade)

    # 2. Contagem global de entidades
    def test_deve_retornar_quantidade_de_entidades_cadastradas(self) -> None:
        qtd_inicial = self.facade.obter_quantidade_entidades()
        self.assertEqual(qtd_inicial["total"], 0)

        self.facade.cadastrar_usuario("aluno", "2026100", "Joao", "joao@ufpb.br", "joaof", "Password@123")
        self.facade.cadastrar_livro("978-01", "Clean Code", "Robert C. Martin", 2008)

        qtd_atualizada = self.facade.obter_quantidade_entidades()
        self.assertEqual(qtd_atualizada["usuarios"], 1)
        self.assertEqual(qtd_atualizada["livros"], 1)
        self.assertEqual(qtd_atualizada["total"], 2)

    # 3. CRUD Livro - Ciclo Completo
    def test_crud_completo_livro_com_sucesso(self) -> None:
        livro = self.facade.cadastrar_livro("978-02", "Pragmatic Programmer", "Andy Hunt", 1999)
        self.assertEqual(livro.titulo, "Pragmatic Programmer")

        encontrado = self.facade.buscar_livro_por_isbn("978-02")
        self.assertEqual(encontrado.autor, "Andy Hunt")

        atualizado = self.facade.atualizar_livro("978-02", titulo="Pragmatic Programmer 20th", ano=2019)
        self.assertEqual(atualizado.titulo, "Pragmatic Programmer 20th")
        self.assertEqual(atualizado.ano, 2019)

        removido = self.facade.remover_livro("978-02")
        self.assertTrue(removido)
        self.assertEqual(len(self.facade.listar_livros()), 0)

    # 4. Duplicidade de ISBN
    def test_deve_lancar_excecao_para_isbn_duplicado(self) -> None:
        self.facade.cadastrar_livro("123", "Livro A", "Autor A", 2020)
        with self.assertRaises(LivroDuplicadoException):
            self.facade.cadastrar_livro("123", "Livro B", "Autor B", 2021)

    # 5. Busca de Livro Inexistente
    def test_deve_lancar_excecao_para_livro_inexistente(self) -> None:
        with self.assertRaises(LivroNaoEncontradoException):
            self.facade.buscar_livro_por_isbn("999999")

    # 6. Remoção de Livro Emprestado
    def test_deve_lancar_excecao_ao_remover_livro_emprestado(self) -> None:
        self.facade.cadastrar_usuario("aluno", "MAT01", "Aluno Teste", "teste@ufpb.br", "alunoteste", "Strong#2026")
        self.facade.cadastrar_livro("456", "Refactoring", "Martin Fowler", 2018)
        self.facade.emprestar_livro("456", "MAT01")

        with self.assertRaises(LivroInvalidoException):
            self.facade.remover_livro("456")

    # 7. Fluxo de Empréstimo e Devolução
    def test_deve_realizar_emprestimo_e_devolucao_com_sucesso(self) -> None:
        self.facade.cadastrar_usuario("aluno", "MAT10", "Carlos Lima", "carlos@ufpb.br", "carlosl", "SenhaForte@1")
        self.facade.cadastrar_livro("789", "Design Patterns", "GoF", 1994)

        livro_emprestado = self.facade.emprestar_livro("789", "MAT10")
        self.assertTrue(livro_emprestado.esta_emprestado)
        self.assertEqual(livro_emprestado.matricula_locatario, "MAT10")

        livro_devolvido = self.facade.devolver_livro("789")
        self.assertFalse(livro_devolvido.esta_emprestado)
        self.assertIsNone(livro_devolvido.matricula_locatario)

    # 8. Empréstimo para Usuário Inexistente
    def test_deve_lancar_excecao_ao_emprestar_para_usuario_inexistente(self) -> None:
        self.facade.cadastrar_livro("111", "Domain-Driven Design", "Eric Evans", 2003)
        with self.assertRaises(DadosUsuarioInvalidosException):
            self.facade.emprestar_livro("111", "MAT_FANTASMA")

    # 9. Conflito de Empréstimo Duplo
    def test_deve_lancar_excecao_ao_emprestar_livro_ja_emprestado(self) -> None:
        self.facade.cadastrar_usuario("aluno", "MAT01", "Aluno A", "a@ufpb.br", "alunoa", "SenhaForte@1")
        self.facade.cadastrar_usuario("aluno", "MAT02", "Aluno B", "b@ufpb.br", "alunob", "SenhaForte@2")
        self.facade.cadastrar_livro("222", "Clean Architecture", "Robert Martin", 2017)

        self.facade.emprestar_livro("222", "MAT01")
        with self.assertRaises(LivroInvalidoException):
            self.facade.emprestar_livro("222", "MAT02")

    # 10. Devolução de Obra Não Emprestada
    def test_deve_lancar_excecao_ao_devolver_livro_nao_emprestado(self) -> None:
        self.facade.cadastrar_livro("333", "Extreme Programming", "Kent Beck", 2000)
        with self.assertRaises(LivroInvalidoException):
            self.facade.devolver_livro("333")

    # 11. Persistência e Recuperação em Arquivo Binário (.bin)
    def test_deve_persistir_livros_em_arquivo_binario(self) -> None:
        FacadeSingletonController.reset_instance()
        repo_user_bin = UsuarioRepositoryBinary(self.ARQUIVO_USUARIOS_TESTE)
        repo_livro_bin = LivroRepositoryBinary(self.ARQUIVO_LIVROS_TESTE)
        facade_bin = FacadeSingletonController(repo_user_bin, repo_livro_bin)

        facade_bin.cadastrar_livro("BIN-01", "Livro Binario", "Autor Binario", 2024)

        FacadeSingletonController.reset_instance()
        repo_livro_reaberto = LivroRepositoryBinary(self.ARQUIVO_LIVROS_TESTE)
        repo_user_reaberto = UsuarioRepositoryBinary(self.ARQUIVO_USUARIOS_TESTE)
        facade_reaberta = FacadeSingletonController(repo_user_reaberto, repo_livro_reaberto)

        livro_recuperado = facade_reaberta.buscar_livro_por_isbn("BIN-01")
        self.assertIsNotNone(livro_recuperado)
        self.assertEqual(livro_recuperado.titulo, "Livro Binario")

    # 12. Limite de Caracteres de Login (12 vs 13)
    def test_fronteira_login_maximo_doze_caracteres(self) -> None:
        usuario_valido = self.facade.cadastrar_usuario(
            "aluno", "M12", "Nome", "m12@ufpb.br", "abcdefghijkl", "SenhaForte@1"
        )
        self.assertEqual(usuario_valido.login, "abcdefghijkl")

        with self.assertRaises(LoginInvalidoException):
            self.facade.cadastrar_usuario(
                "aluno", "M13", "Nome", "m13@ufpb.br", "abcdefghijklm", "SenhaForte@1"
            )

    # 13. Decremento Dinâmico na Contagem da Fachada após Deleção
    def test_deve_decrementar_total_de_entidades_apos_remocao_de_livro(self) -> None:
        self.facade.cadastrar_livro("DEL-01", "Livro Temporario", "Autor", 2021)
        self.assertEqual(self.facade.obter_quantidade_entidades()["livros"], 1)

        self.facade.remover_livro("DEL-01")
        self.assertEqual(self.facade.obter_quantidade_entidades()["livros"], 0)
        self.assertEqual(self.facade.obter_quantidade_entidades()["total"], 0)

    # 14. Validação de Ano Inválido no Livro
    def test_deve_lancar_excecao_para_ano_invalido_de_livro(self) -> None:
        with self.assertRaises(LivroInvalidoException):
            self.facade.cadastrar_livro("ANO-INV-1", "Titulo", "Autor", -50)

        with self.assertRaises(LivroInvalidoException):
            self.facade.cadastrar_livro("ANO-INV-2", "Titulo", "Autor", 3000)

    # 15. Filtro de Livros por Locatário
    def test_deve_listar_livros_por_locatario(self) -> None:
        self.facade.cadastrar_usuario("aluno", "LOC01", "Aluno Um", "u1@ufpb.br", "alunoum", "SenhaForte@1")
        self.facade.cadastrar_livro("LIV01", "Livro 1", "Autor", 2020)
        self.facade.cadastrar_livro("LIV02", "Livro 2", "Autor", 2021)
        self.facade.cadastrar_livro("LIV03", "Livro 3", "Autor", 2022)

        self.facade.emprestar_livro("LIV01", "LOC01")
        self.facade.emprestar_livro("LIV02", "LOC01")

        livros_locatario = self.facade.listar_livros_por_locatario("LOC01")
        self.assertEqual(len(livros_locatario), 2)

        livros_outro = self.facade.listar_livros_por_locatario("LOC_SEM_NADA")
        self.assertEqual(len(livros_outro), 0)

    # 16. Verificação de Especialização Aluno vs Professor
    def test_deve_instanciar_corretamente_especializacoes_com_limites_distintos(self) -> None:
        aluno = self.facade.cadastrar_usuario("aluno", "A01", "Aluno", "a@ufpb.br", "alunolim", "SenhaForte@1")
        professor = self.facade.cadastrar_usuario("professor", "P01", "Prof", "p@ufpb.br", "proflim", "SenhaForte@1")

        self.assertEqual(aluno.limite_livros, 3)
        self.assertEqual(professor.limite_livros, 5)
        self.assertEqual(aluno.obter_tipo(), "Aluno")
        self.assertEqual(professor.obter_tipo(), "Professor")


if __name__ == "__main__":
    unittest.main()