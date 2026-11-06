from src.application.services.usuario_service import UsuarioService
from src.domain.exceptions.usuario_exceptions import UsuarioException


class UserCLI:
    def __init__(self, servico: UsuarioService, nome_mecanismo: str) -> None:
        self._servico = servico
        self._nome_mecanismo = nome_mecanismo

    def exibir_menu(self) -> None:
        print(f"\n=== SISTEMA DE BIBLIOTECA [{self._nome_mecanismo}] ===")
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
                login = input("Login (máx 12 letras, sem números): ").strip()
                senha = input("Senha (política AWS IAM): ").strip()

                try:
                    usuario = self._servico.cadastrar_usuario(
                        tipo=tipo,
                        matricula=matricula,
                        nome=nome,
                        email=email,
                        login=login,
                        senha=senha
                    )
                    print(f"Sucesso: {usuario.obter_tipo()} '{usuario.login}' cadastrado com sucesso!")
                except UsuarioException as erro:
                    print(f"Erro de validação: {erro}")
                except Exception as erro_inesperado:
                    print(f"Erro no sistema: {erro_inesperado}")

            elif opcao == "3":
                try:
                    usuarios = self._servico.listar_usuarios()
                    if not usuarios:
                        print("Nenhum usuário cadastrado.")
                    else:
                        print(f"\n--- Usuários Cadastrados ({self._nome_mecanismo}) ---")
                        for u in usuarios:
                            print(
                                f"[{u.obter_tipo()}] Matrícula: {u.matricula} | "
                                f"Login: {u.login} | Nome: {u.nome} | "
                                f"E-mail: {u.email} | Limite: {u.limite_livros} livros"
                            )
                except UsuarioException as erro:
                    print(f"Erro ao acessar persistência: {erro}")

            else:
                print("Opção inválida. Tente novamente.")