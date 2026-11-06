# Especificacao do Sistema de Gerenciamento de Biblioteca

## 1. Casos de Uso do Sistema

Atores:
- Bibliotecario: Administrador do acervo e registros.
- Usuario: Entidade base que pode ser Aluno ou Professor.

### Casos de Uso de Usuarios:
- UC01 - Cadastrar Usuario: O Bibliotecario cadastra Aluno ou Professor com matricula, nome, email, login e senha forte (politica AWS IAM).
- UC02 - Listar Usuarios: Exibe todos os usuarios do mecanismo ativo.
- UC03 - Buscar Usuario por Matricula: Localiza usuario pela matricula institucional.

### Casos de Uso de Livros (CRUD):
- UC04 - Cadastrar Livro: Registra livro com ISBN unico, titulo, autor e ano.
- UC05 - Buscar Livro por ISBN: Consulta informacoes detalhadas da obra.
- UC06 - Atualizar Livro: Permite alterar dados da obra ou associar um usuario locatario.
- UC07 - Remover Livro: Remove a obra do acervo caso nao esteja emprestada.
- UC08 - Listar Livros: Lista todas as obras ou filtra por usuario locatario.

---

## 2. Diagrama de Classes e Arquitetura (Sprint 3 - Facade & Singleton)

Relacoes estruturais:
- FacadeSingletonController (Singleton & Facade):
  Ponto de acesso unico para todas as operacoes de controle da aplicacao.
  + get_instance(usuario_repo, livro_repo)
  + obter_quantidade_entidades(): dict (retorna total de usuarios e livros cadastrados)
  + operacoes delegadas para UsuarioService e LivroService

- Controladores / Servicos:
  * UsuarioService: regras de validacao de login/senha e persistencia de usuarios.
  * LivroService: regras de validacao, integridade de ISBN e CRUD completo de livros.

- Repositorios (Interfaces e Persistencia desacoplada):
  * IUsuarioRepository -> UsuarioRepositoryMemory / UsuarioRepositoryBinary
  * ILivroRepository   -> LivroRepositoryMemory   / LivroRepositoryBinary

- Entidades:
  * Usuario (Aluno, Professor)
  * Livro (isbn, titulo, autor, ano, matricula_locatario)

---

## 3. Politicas de Validacao e Excecoes

- Usuario:
  * LoginInvalidoException: login vazio, > 12 chars ou com digitos numericos.
  * SenhaFracaException: violacao das regras de complexidade AWS IAM.
  * UsuarioDuplicadoException: matricula, email ou login duplicados.

- Livro:
  * LivroInvalidoException: dados obrigatorios vazios ou ano inconsistente.
  * LivroDuplicadoException: ISBN ja existente no acervo.
  * LivroNaoEncontradoException: busca/edicao/remocao de ISBN inexistente.

- Persistencia:
  * PersistenciaException: falhas de leitura/escrita em arquivo binario (.bin).