import unittest
from src.application.services.usuario_service import UsuarioService
from src.domain.entities.usuario import Aluno, Professor
from src.domain.exceptions.usuario_exceptions import (
    DadosUsuarioInvalidosException,
    UsuarioDuplicadoException,
)
from src.infrastructure.memory.usuario_repository_memory import UsuarioRepositoryMemory


class TestUsuarioService(unittest.TestCase):
    def setUp(self) -> None:
        self.repositorio = UsuarioRepositoryMemory()
        self.servico = UsuarioService(self.repositorio)

    def test_deve_cadastrar_aluno_com_sucesso(self) -> None:
        usuario = self.servico.cadastrar_usuario(
            tipo="aluno",
            matricula="2026001",
            nome="Carlos Silva",
            email="carlos@ufpb.br"
        )
        self.assertIsInstance(usuario, Aluno)
        self.assertEqual(usuario.matricula, "2026001")
        self.assertEqual(usuario.limite_livros, 3)
        self.assertEqual(len(self.servico.listar_usuarios()), 1)

    def test_deve_cadastrar_professor_com_sucesso(self) -> None:
        usuario = self.servico.cadastrar_usuario(
            tipo="professor",
            matricula="PROF100",
            nome="Dra. Ana Pereira",
            email="ana@ufpb.br"
        )
        self.assertIsInstance(usuario, Professor)
        self.assertEqual(usuario.matricula, "PROF100")
        self.assertEqual(usuario.limite_livros, 5)

    def test_deve_listar_todos_os_usuarios_cadastrados(self) -> None:
        self.assertEqual(len(self.servico.listar_usuarios()), 0)
        self.servico.cadastrar_usuario("aluno", "A01", "Aluno Um", "a1@ufpb.br")
        self.servico.cadastrar_usuario("professor", "P01", "Prof Um", "p1@ufpb.br")
        
        lista = self.servico.listar_usuarios()
        self.assertEqual(len(lista), 2)

    def test_deve_lancar_excecao_ao_cadastrar_matricula_duplicada(self) -> None:
        self.servico.cadastrar_usuario("aluno", "MAT10", "Joao", "joao@ufpb.br")
        with self.assertRaises(UsuarioDuplicadoException):
            self.servico.cadastrar_usuario("professor", "MAT10", "Outro Nome", "outro@ufpb.br")

    def test_deve_lancar_excecao_ao_cadastrar_email_duplicado(self) -> None:
        self.servico.cadastrar_usuario("aluno", "MAT10", "Joao", "joao@ufpb.br")
        with self.assertRaises(UsuarioDuplicadoException):
            self.servico.cadastrar_usuario("aluno", "MAT11", "Outro Joao", "joao@ufpb.br")

    def test_deve_lancar_excecao_quando_dados_estiverem_vazios(self) -> None:
        with self.assertRaises(DadosUsuarioInvalidosException):
            self.servico.cadastrar_usuario("aluno", "", "Nome", "email@ufpb.br")

        with self.assertRaises(DadosUsuarioInvalidosException):
            self.servico.cadastrar_usuario("aluno", "123", "", "email@ufpb.br")

        with self.assertRaises(DadosUsuarioInvalidosException):
            self.servico.cadastrar_usuario("aluno", "123", "Nome", "emailsemarroba")

    def test_deve_lancar_excecao_quando_tipo_for_invalido(self) -> None:
        with self.assertRaises(DadosUsuarioInvalidosException):
            self.servico.cadastrar_usuario("diretor", "DIR01", "Nome", "dir@ufpb.br")


if __name__ == "__main__":
    unittest.main()