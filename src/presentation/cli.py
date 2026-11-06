from src.application.services.facade_singleton_controller import FacadeSingletonController
from src.domain.exceptions.livro_exceptions import LivroException
from src.domain.exceptions.usuario_exceptions import UsuarioException


class UserCLI:
    def __init__(self, facade: FacadeSingletonController, nome_mecanismo: str) -> None:
        self._facade = facade
        self._nome_mecanismo = nome_mecanismo

    def exibir_menu(self) -> None:
        totais = self._facade.obter_quantidade_entidades()
        print(f"\n=======================================================")
        print(f" SISTEMA DE BIBLIOTECA [{self._nome_mecanismo}]")
        print(f" Total no Acervo: {totais['total']} entidades ({totais['usuarios']} usuários | {totais['livros']} livros)")
        print(f"=======================================================")
        print("--- Gerenciamento de Usuários ---")
        print("1. Cadastrar Aluno")
        print("2. Cadastrar Professor")
        print("3. Listar Todos os Usuários")
        print("\n--- Gerenciamento de Livros (CRUD) ---")
        print("4. Cadastrar Livro")
        print("5. Listar Todos os Livros")
        print("6. Consultar Livro por ISBN")
        print("7. Atualizar Dados de Livro")
        print("8. Remover Livro")
        print("9. Emprestar Livro a Usuário")
        print("10. Devolver Livro")
        print("\n0. Sair")

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
                    usuario = self._facade.cadastrar_usuario(
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
                usuarios = self._facade.listar_usuarios()
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

            elif opcao == "4":
                isbn = input("ISBN: ").strip()
                titulo = input("Título: ").strip()
                autor = input("Autor: ").strip()
                ano_str = input("Ano de publicação: ").strip()

                try:
                    ano = int(ano_str)
                    livro = self._facade.cadastrar_livro(isbn, titulo, autor, ano)
                    print(f"Sucesso: Livro '{livro.titulo}' ({livro.isbn}) cadastrado!")
                except (LivroException, ValueError) as erro:
                    print(f"Erro ao cadastrar livro: {erro}")

            elif opcao == "5":
                livros = self._facade.listar_livros()
                if not livros:
                    print("Nenhum livro cadastrado.")
                else:
                    print(f"\n--- Acervo de Livros ({self._nome_mecanismo}) ---")
                    for l in livros:
                        status = f"Emprestado para matrícula {l.matricula_locatario}" if l.esta_emprestado else "Disponível"
                        print(f"ISBN: {l.isbn} | Título: {l.titulo} | Autor: {l.autor} | Ano: {l.ano} | Status: {status}")

            elif opcao == "6":
                isbn = input("Digite o ISBN: ").strip()
                try:
                    livro = self._facade.buscar_livro_por_isbn(isbn)
                    status = f"Emprestado para matrícula {livro.matricula_locatario}" if livro.esta_emprestado else "Disponível"
                    print(f"\nISBN: {livro.isbn}\nTítulo: {livro.titulo}\nAutor: {livro.autor}\nAno: {livro.ano}\nStatus: {status}")
                except LivroException as erro:
                    print(f"Erro: {erro}")

            elif opcao == "7":
                isbn = input("ISBN do livro a atualizar: ").strip()
                print("Deixe em branco os campos que não deseja alterar:")
                titulo = input("Novo título: ").strip() or None
                autor = input("Novo autor: ").strip() or None
                ano_str = input("Novo ano: ").strip()
                ano = int(ano_str) if ano_str else None

                try:
                    livro = self._facade.atualizar_livro(isbn, titulo, autor, ano)
                    print(f"Sucesso: Livro '{livro.isbn}' atualizado!")
                except (LivroException, ValueError) as erro:
                    print(f"Erro ao atualizar livro: {erro}")

            elif opcao == "8":
                isbn = input("ISBN do livro a remover: ").strip()
                try:
                    self._facade.remover_livro(isbn)
                    print(f"Sucesso: Livro '{isbn}' removido do acervo!")
                except LivroException as erro:
                    print(f"Erro ao remover livro: {erro}")

            elif opcao == "9":
                isbn = input("ISBN do livro: ").strip()
                matricula = input("Matrícula do usuário: ").strip()
                try:
                    livro = self._facade.emprestar_livro(isbn, matricula)
                    print(f"Sucesso: Livro '{livro.titulo}' associado ao usuário '{matricula}'!")
                except (LivroException, UsuarioException) as erro:
                    print(f"Erro no empréstimo: {erro}")

            elif opcao == "10":
                isbn = input("ISBN do livro a devolver: ").strip()
                try:
                    livro = self._facade.devolver_livro(isbn)
                    print(f"Sucesso: Livro '{livro.titulo}' devolvido ao acervo!")
                except LivroException as erro:
                    print(f"Erro na devolução: {erro}")

            else:
                print("Opção inválida. Tente novamente.")