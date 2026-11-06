from src.application.services.usuario_service import UsuarioService
from src.domain.exceptions.usuario_exceptions import UsuarioException


class UserCLI:
    def __init__(self, servico: UsuarioService) -> None:
        self._servico = servico

    def exibir_menu(self) -> None:
        print("\n=== SISTEMA DE BIBLIOTECA ===")
        print("1. Cadastrar Aluno")
        print("2. Cadastrar Professor")
        print("3. Listar Todos os Usuários")
        print("0. Sair")

    def executar(self) -> None:
        while True:
            self.exibir_menu()
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "0":
                print("Encerrando o sistema...")
                break

            elif opcao in ("1", "2"):
                tipo = "aluno" if opcao == "1" else "professor"
                matricula = input("Matrícula: ").strip()
                nome = input("Nome: ").strip()
                email = input("E-mail: ").strip()

                try:
                    usuario = self._servico.cadastrar_usuario(
                        tipo=tipo,
                        matricula=matricula,
                        nome=nome,
                        email=email
                    )
                    print(f"Sucesso: {usuario.obter_tipo()} cadastrado (Limite de livros: {usuario.limite_livros}).")
                except UsuarioException as erro:
                    print(f"Erro de validação: {erro}")

            elif opcao == "3":
                usuarios = self._servico.listar_usuarios()
                if not usuarios:
                    print("Nenhum usuário cadastrado.")
                else:
                    print("\n--- Usuários Cadastrados na Memória RAM ---")
                    for u in usuarios:
                        print(f"[{u.obter_tipo()}] Matrícula: {u.matricula} | Nome: {u.nome} | E-mail: {u.email} | Limite: {u.limite_livros} livros")

            else:
                print("Opção inválida. Tente novamente.")