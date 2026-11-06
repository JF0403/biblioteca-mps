# Especificacao do Sistema de Gerenciamento de Biblioteca

## 1. Casos de Uso - Gerenciamento de Usuarios

Atores:
- Bibliotecario: Administrador do acervo e registros.
- Usuario: Entidade base que pode ser Aluno ou Professor.

### Descricao dos Casos de Uso:
- UC01 - Cadastrar Usuario: O Bibliotecario cadastra Aluno ou Professor informando nome, email e matricula. O sistema valida duplicidade de email e matricula.
- UC02 - Listar Usuarios: O sistema lista todos os usuarios persistidos na memoria RAM.
- UC03 - Buscar Usuario por Matricula: Permite localizar uma entidade de usuario atraves da matricula institucional.

## 2. Analise de Classes BCE (Fronteira, Controle, Entidade)

- Fronteira (Boundary): UserCLI - interface de linha de comando para interacao.
- Controle (Control): UsuarioService (regras de validacao de negocio) e IUsuarioRepository (abstracao de persistencia).
- Entidade (Entity): Usuario (base abstrata), Aluno (especializacao) e Professor (especializacao).
- Persistencia: UsuarioRepositoryMemory (colecao em RAM).