import os
import unittest
from src.application.services.usuario_service import UsuarioService
from src.domain.entities.usuario import Aluno, Professor
from src.domain.exceptions.usuario_exceptions import (
    DadosUsuarioInvalidosException,
    LoginInvalidoException,
    SenhaFracaException,
    UsuarioDuplicadoException,
)
from src.infrastructure.binary.usuario_repository_binary import UsuarioRepositoryBinary
from src.infrastructure.memory.usuario_repository_memory import UsuarioRepositoryMemory


class TestUsuarioServiceBase:
    def test_deve_cadastrar_aluno_com_sucesso(self) -> None:
        usuario = self.servico.cadastrar_usuario(
            tipo="aluno",
            matricula="2026001",
            nome="Carlos Silva",
            email="carlos@ufpb.br",
            login="carlos",
            senha="Password@123"
        )
        self.assertIsInstance(usuario, Aluno)
        self.assertEqual(usuario.matricula, "2026001")
        self.assertEqual(usuario.login, "carlos")
        self.assertEqual(usuario.limite_livros, 3)

    def test_deve_cadastrar_professor_com_sucesso(self) -> None:
        usuario = self.servico.cadastrar_usuario(
            tipo="professor",
            matricula="PROF100",
            nome="Dra. Ana",
            email="ana@ufpb.br",
            login="anaprof",
            senha="Complex#2026"
        )
        self.assertIsInstance(usuario, Professor)
        self.assertEqual(usuario.matricula, "PROF100")
        self.assertEqual(usuario.limite_livros, 5)

    def test_deve_lancar_excecao_para_login_com_numeros(self) -> None:
        with self.assertRaises(LoginInvalidoException):
            self.servico.cadastrar_usuario(
                tipo="aluno",
                matricula="M01",
                nome="Lucas",
                email="lucas@ufpb.br",
                login="lucas123",
                senha="Password@123"
            )

    def test_deve_lancar_excecao_para_login_com_mais_de_12_caracteres(self) -> None:
        with self.assertRaises(LoginInvalidoException):
            self.servico.cadastrar_usuario(
                tipo="aluno",
                matricula="M02",
                nome="Fernando",
                email="fernando@ufpb.br",
                login="nomecompletomuitolongo",
                senha="Password@123"
            )

    def test_deve_lancar_excecao_para_login_vazio(self) -> None:
        with self.assertRaises(LoginInvalidoException):
            self.servico.cadastrar_usuario(
                tipo="aluno",
                matricula="M03",
                nome="Marcos",
                email="marcos@ufpb.br",
                login="   ",
                senha="Password@123"
            )

    def test_deve_lancar_excecao_quando_senha_nao_atende_politica_aws(self) -> None:
        # Menos de 8 caracteres
        with self.assertRaises(SenhaFracaException):
            self.servico.cadastrar_usuario("aluno", "M1", "A", "a@ufpb.br", "useraluno", "Aa1!")

        # Sem maiúscula
        with self.assertRaises(SenhaFracaException):
            self.servico.cadastrar_usuario("aluno", "M2", "A", "b@ufpb.br", "useraluno", "password@123")

        # Sem minúscula
        with self.assertRaises(SenhaFracaException):
            self.servico.cadastrar_usuario("aluno", "M3", "A", "c@ufpb.br", "useraluno", "PASSWORD@123")

        # Sem número
        with self.assertRaises(SenhaFracaException):
            self.servico.cadastrar_usuario("aluno", "M4", "A", "d@ufpb.br", "useraluno", "Password@abc")

        # Sem caractere especial
        with self.assertRaises(SenhaFracaException):
            self.servico.cadastrar_usuario("aluno", "M5", "A", "e@ufpb.br", "useraluno", "Password123")

        # Senha igual ao login
        with self.assertRaises(SenhaFracaException):
            self.servico.cadastrar_usuario("aluno", "M6", "A", "f@ufpb.br", "meulogin", "meulogin")

    def test_deve_lancar_excecao_para_login_duplicado(self) -> None:
        self.servico.cadastrar_usuario("aluno", "M1", "Nome 1", "u1@ufpb.br", "usuario", "Password@123")
        with self.assertRaises(UsuarioDuplicadoException):
            self.servico.cadastrar_usuario("professor", "M2", "Nome 2", "u2@ufpb.br", "usuario", "Password@123")


class TestUsuarioServiceMemory(TestUsuarioServiceBase, unittest.TestCase):
    def setUp(self) -> None:
        self.repositorio = UsuarioRepositoryMemory()
        self.servico = UsuarioService(self.repositorio)


class TestUsuarioServiceBinary(TestUsuarioServiceBase, unittest.TestCase):
    CAMINHO_TESTE = "teste_usuarios.bin"

    def setUp(self) -> None:
        if os.path.exists(self.CAMINHO_TESTE):
            os.remove(self.CAMINHO_TESTE)
        self.repositorio = UsuarioRepositoryBinary(self.CAMINHO_TESTE)
        self.servico = UsuarioService(self.repositorio)

    def tearDown(self) -> None:
        if os.path.exists(self.CAMINHO_TESTE):
            os.remove(self.CAMINHO_TESTE)


if __name__ == "__main__":
    unittest.main()