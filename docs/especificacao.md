# Especificacao do Sistema de Gerenciamento de Biblioteca

## 1. Casos de Uso - Gerenciamento de Usuarios

Atores:
- Bibliotecario: Administrador do acervo e registos.
- Usuario: Entidade base que pode ser Aluno ou Professor.

### Descricao dos Casos de Uso:
- UC01 - Cadastrar Usuario: O Bibliotecario cadastra Aluno ou Professor informando nome, email, matricula, login e senha. O sistema valida regras estritas de formato e unicidade.
- UC02 - Listar Usuarios: O sistema lista todos os usuarios persistidos no mecanismo ativo (RAM ou Ficheiro Binario).
- UC03 - Buscar Usuario por Matricula: Permite localizar uma entidade atraves da matricula institucional.

## 2. Diagrama de Classes e Arquitetura (Sprint 2)

Relacoes estruturais:
- IUsuarioRepository (Interface):
  + salvar(usuario)
  + buscar_por_matricula(matricula)
  + buscar_por_login(login)
  + buscar_por_email(email)
  + listar_todos()

- Implementacoes de IUsuarioRepository:
  * UsuarioRepositoryMemory (colecao em memoria RAM)
  * UsuarioRepositoryBinary (colecao persistida em ficheiro binario .bin, tratando IOError/OSError e lancando PersistenciaException)

- UsuarioService (Controlo e Regras):
  * Valida formato do login (max 12 caracteres, sem digitos numericos)
  * Valida complexidade da senha (politica AWS IAM: min 8 caracteres, maiuscula, minuscula, numero, simbolo e diferente do login)
  * Valida unicidade de matricula, email e login

- Entidades de Dominio:
  * Usuario (classe base com matricula, nome, email, login, senha, limite_livros)
  * Aluno (especializacao com limite de 3 livros)
  * Professor (especializacao com limite de 5 livros)

## 3. Politicas de Validacao e Excecoes de Dominio

- LoginInvalidoException: Login vazio, superior a 12 caracteres ou contendo algarismos.
- SenhaFracaException: Senha com menos de 8 caracteres, sem variedade de classes de caracteres ou identica ao login.
- UsuarioDuplicadoException: Matricula, email ou login ja existentes.
- PersistenciaException: Falhas de leitura/escrita em disco no repositorio binario.
