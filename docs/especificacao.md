# Especificação do Sistema de Gerenciamento de Biblioteca

## 1. Casos de Uso do Sistema

Atores:
- Bibliotecário: Responsável pela administração do acervo e registros.
- Usuário: Entidade base especializada em Aluno (limite de 3 livros) ou Professor (limite de 5 livros).

### Especificação Detalhada dos Casos de Uso Principais

#### UC01 - Cadastrar Usuário com Credenciais AWS IAM
- Ator: Bibliotecário.
- Pré-condições: Repositório inicializado.
- Pós-condições: Usuário criado com limite de empréstimo conforme especialização.
- Fluxo Principal:
  1. O Bibliotecário informa matrícula, nome, e-mail, login e senha.
  2. O sistema valida os dados gerais de identificação.
  3. O sistema valida o login (máx. 12 caracteres, não vazio e sem algarismos).
  4. O sistema valida a complexidade da senha conforme a política AWS IAM (8+ caracteres, maiúscula, minúscula, dígito, símbolo e diferente do login).
  5. O sistema assegura unicidade de matrícula, e-mail e login.
  6. O usuário é persistido no repositório ativo.

#### UC04 - Cadastrar Livro no Acervo (CRUD)
- Ator: Bibliotecário.
- Pré-condições: Nenhuma.
- Pós-condições: Livro registrado no catálogo como disponível.
- Fluxo Principal:
  1. O Bibliotecário fornece ISBN, título, autor e ano.
  2. O sistema valida formato e preenchimento obrigatório dos campos.
  3. O sistema assegura a unicidade do ISBN.
  4. A obra é armazenada no mecanismo ativo.

#### UC09 - Emprestar Livro
- Ator: Bibliotecário.
- Pré-condições: Livro e usuário devem existir previamente no sistema.
- Pós-condições: O livro é associado à matrícula do locatário.
- Fluxo Principal:
  1. O Bibliotecário informa o ISBN e a matrícula do usuário.
  2. O sistema valida a disponibilidade do livro e a existência do usuário.
  3. O vínculo é registrado e persistido.

---

## 2. Diagrama de Casos de Uso (Mapeamento de Requisitos)

- RF01 / UC01: Cadastrar Usuário (Aluno / Professor) [inclui Validação IAM]
- RF02 / UC02: Listar Usuários
- RF03 / UC03: Consultar Usuário por Matrícula
- RF04 / UC04: Cadastrar Livro
- RF05 / UC05: Consultar Livro por ISBN
- RF06 / UC06: Atualizar Livro
- RF07 / UC07: Remover Livro (valida se não está emprestado)
- RF08 / UC08: Listar Acervo Completo
- RF09 / UC09: Emprestar Livro (associa Livro a Usuário)
- RF10 / UC10: Devolver Livro
- RF11 / UC11: Obter Quantitativo Geral de Entidades

---

## 3. Diagrama de Classes de Análise (BCE + Facade & Singleton)

### Camada de Apresentação (Boundary):
- `UserCLI`: Interface em linha de comando desacoplada que se comunica exclusivamente com a Facade.

### Camada de Aplicação / Controle (Control):
- `FacadeSingletonController` (Padrões Facade + Singleton):
  * Instância única global (`__new__`, `get_instance()`).
  * Ponto de orquestração unificado para os serviços.
  * Método obrigatório: `obter_quantidade_entidades() -> dict`.
- `UsuarioService`: Gerenciador de regras de negócio, unicidade e validações de credenciais.
- `LivroService`: Gerenciador do CRUD de livros, integridade de acervo e operações de empréstimo.

### Camada de Domínio (Entity):
- `Usuario` (abstrata): Atributos comuns (`matricula`, `nome`, `email`, `login`, `senha`, `limite_livros`).
  * `Aluno`: limite de 3 livros.
  * `Professor`: limite de 5 livros.
- `Livro`: Atributos (`isbn`, `titulo`, `autor`, `ano`, `matricula_locatario`).
  * Métodos de controle de estado: `esta_emprestado`, `associar_locatario`, `desassociar_locatario`.

### Camada de Infraestrutura:
- Contratos Abstratos: `IUsuarioRepository`, `ILivroRepository`.
- Persistência em Memória RAM: `UsuarioRepositoryMemory`, `LivroRepositoryMemory`.
- Persistência em Disco Binário: `UsuarioRepositoryBinary`, `LivroRepositoryBinary` (tratando falhas de I/O e gerando `PersistenciaException`).

---

## 4. Matriz de Exceções de Domínio

| Exceção | Gatilho de Disparo |
| :--- | :--- |
| `LoginInvalidoException` | Login vazio, com mais de 12 caracteres ou contendo algarismos numéricos. |
| `SenhaFracaException` | Senha com menos de 8 caracteres, sem maiúscula/minúscula/número/símbolo ou igual ao login. |
| `UsuarioDuplicadoException` | Matrícula, e-mail ou login já cadastrados. |
| `LivroInvalidoException` | Campos obrigatórios vazios, ano incoerente ou tentativa de remoção de obra emprestada. |
| `LivroDuplicadoException` | Tentativa de cadastro de ISBN já existente. |
| `LivroNaoEncontradoException`| Consulta, atualização ou empréstimo referenciando ISBN inexistente. |
| `PersistenciaException` | Falhas de gravação/leitura no arquivo binário (`.bin`). |