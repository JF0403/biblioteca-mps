# Especificação do Sistema de Gerenciamento de Biblioteca

## 1. Casos de Uso do Sistema

Atores:
- Bibliotecário: Responsável pela administração do acervo, registros e geração de relatórios.
- Usuário: Entidade base especializada em Aluno (limite de 3 livros) ou Professor (limite de 5 livros).

### Especificação Detalhada dos Casos de Uso Principais

#### UC01 - Cadastrar Usuário com Credenciais AWS IAM
- Ator: Bibliotecário.
- Pré-condições: Repositório inicializado via `RepositoryFactory`.
- Pós-condições: Usuário criado com limite de empréstimo conforme especialização e evento registrado via `ILogger`.
- Fluxo Principal:
  1. O Bibliotecário informa matrícula, nome, e-mail, login e senha.
  2. A fachada encapsula a requisição em `CadastrarUsuarioCommand` e a envia ao `CommandInvoker`.
  3. O sistema valida os dados gerais de identificação e o login (máx. 12 caracteres, não vazio e sem algarismos).
  4. O sistema valida a complexidade da senha conforme a política AWS IAM (8+ caracteres, maiúscula, minúscula, dígito, símbolo e diferente do login).
  5. O sistema assegura unicidade de matrícula, e-mail e login e persiste o usuário no repositório ativo.

#### UC04 - Cadastrar Livro no Acervo (CRUD)
- Ator: Bibliotecário.
- Pré-condições: Nenhuma.
- Pós-condições: Livro registrado no catálogo como disponível.
- Fluxo Principal:
  1. O Bibliotecário fornece ISBN, título, autor e ano.
  2. O sistema valida formato, preenchimento obrigatório e unicidade do ISBN.
  3. A obra é armazenada no mecanismo ativo.

#### UC06 & UC13 - Atualizar Livro e Desfazer Última Atualização (Memento)
- Ator: Bibliotecário.
- Pré-condições: Livro previamente cadastrado no acervo.
- Pós-condições: Dados do livro atualizados (salvando snapshot anterior no `LivroCaretaker`) ou restaurados ao estado imediatamente anterior.
- Fluxo Principal (Atualização):
  1. Antes de aplicar a alteração, `AtualizarLivroCommand` solicita ao `LivroOriginator` a criação de um `LivroMemento`.
  2. O `LivroService` valida e persiste os novos dados.
  3. O snapshot anterior é armazenado no `LivroCaretaker` (substituindo eventual snapshot anterior).
- Fluxo Principal (Desfazer):
  1. O Bibliotecário aciona a opção de desfazer a última atualização.
  2. `DesfazerUltimaAtualizacaoLivroCommand` recupera o último `LivroMemento` do `LivroCaretaker`.
  3. O `LivroOriginator` restaura os atributos originais via `LivroService` e limpa o histórico do zelador.

#### UC09 - Emprestar Livro
- Ator: Bibliotecário.
- Pré-condições: Livro e usuário devem existir previamente no sistema.
- Pós-condições: O livro é associado à matrícula do locatário.
- Fluxo Principal:
  1. O Bibliotecário informa o ISBN e a matrícula do usuário.
  2. O sistema valida a disponibilidade do livro e a existência do usuário.
  3. O vínculo é registrado e persistido.

#### UC12 - Exportar Relatório de Estatísticas (Template Method)
- Ator: Bibliotecário.
- Pré-condições: Nenhuma.
- Pós-condições: Arquivo de relatório gerado em HTML ou TXT com o quantitativo de usuários e livros.
- Fluxo Principal:
  1. O Bibliotecário escolhe o formato (`html` ou `txt`).
  2. `ExportarRelatorioEstatisticasCommand` executa o algoritmo estruturado em `RelatorioEstatisticasTemplate` (`_gerar_cabecalho`, `_gerar_corpo`, `_gerar_rodape`, `_salvar_arquivo`).

---

## 2. Mapeamento de Requisitos Funcionais

- RF01 / UC01: Cadastrar Usuário (Aluno / Professor) [inclui Validação IAM]
- RF02 / UC02: Listar Usuários
- RF03 / UC03: Consultar Usuário por Matrícula
- RF04 / UC04: Cadastrar Livro
- RF05 / UC05: Consultar Livro por ISBN
- RF06 / UC06: Atualizar Livro (com captura de Memento)
- RF07 / UC07: Remover Livro (valida se não está emprestado)
- RF08 / UC08: Listar Acervo Completo
- RF09 / UC09: Emprestar Livro (associa Livro a Usuário)
- RF10 / UC10: Devolver Livro
- RF11 / UC11: Obter Quantitativo Geral de Entidades
- RF12 / UC12: Exportar Relatório de Estatísticas (HTML e TXT via Template Method)
- RF13 / UC13: Desfazer Última Atualização de Livro (via Memento)

---

## 3. Diagrama de Classes de Projeto (BCE + Padrões GoF)

```text
====================================================================================================
                                PADRÕES DE PROJETO (GoF) IMPLEMENTADOS
====================================================================================================
1. <<Singleton>>        : FacadeSingletonController (Instância única global).
2. <<Facade>>           : FacadeSingletonController (Interface unificada da camada de negócio).
3. <<Repository>>       : IUsuarioRepository, ILivroRepository (Isolamento Business <-> Infra).
4. <<Abstract Factory>> : RepositoryFactory (Cria família de repositórios Memory ou Binary).
5. <<Adapter>>          : PythonLoggerAdapter adaptando ILogger (Isola a biblioteca logging).
6. <<Template Method>>  : RelatorioEstatisticasTemplate (Geração de relatórios HTML e TXT).
7. <<Command>>          : Command, CommandInvoker e BibliotecaCommands (Encapsula operações).
8. <<Memento>>          : LivroOriginator, LivroMemento e LivroCaretaker (Desfaz última edição).

====================================================================================================
                                       CAMADA DE APRESENTAÇÃO
====================================================================================================
                                           <<boundary>>
                                             UserCLI
                                                │ (Usa)
================================================│===================================================
                                   CAMADA DE BUSINESS (CONTROLE)
================================================│===================================================
                                                ▼
                                 <<control, Singleton, Facade>>
                                   FacadeSingletonController
                                - _invoker: CommandInvoker
                                - _livro_originator: LivroOriginator
                                - _livro_caretaker: LivroCaretaker
                                - _logger: ILogger
                                + atualizar_livro(...)
                                + desfazer_ultima_atualizacao_livro()
                                                │
                         ┌──────────────────────┴──────────────────────┐
                         │ (cria e envia)                              │ (executa)
                         ▼                                             ▼
                   <<Command>>                                   <<Invoker>>
                     Command                                   CommandInvoker
                  + execute()                                 - _logger: ILogger
                         ▲                                    + executar(comando)
                         │
        ┌────────────────┼────────────────┬───────────────────────────────┐
        │                │                │                               │
<<ConcreteCommand>> <<ConcreteCommand>> <<ConcreteCommand>>      <<ConcreteCommand>>
CadastrarUsuario    AtualizarLivro      DesfazerUltimaAtuali-    ExportarRelatorio-
Command (+ outros)  Command             zacaoLivroCommand        EstatisticasCommand
        │                │                       │                        │
        │                ├──────────┬────────────┘                        │
        ▼                ▼          ▼                                     ▼
   <<control>>      <<control>>  <<Originator>>                   <<Template Method>>
 UsuarioService    LivroService  LivroOriginator             RelatorioEstatisticasTemplate
        │                │       + criar_memento()               + gerar_relatorio()
        │                │       + restaurar_memento()                ▲        ▲
        │                │          │                                 │        │
        │                │          ▼ criam/restauram           Relatorio  Relatorio
        │                │     <<Memento>>                        HTML        TXT
        │                │     LivroMemento
        │                │     - _isbn, _titulo, _autor, _ano
        │                │          ▲ armazena último (0..1)
        │                │          │
        │                │     <<Caretaker>>
        │                │     LivroCaretaker
        │                │     - _ultimo_memento
=========================│==========│===============================================================
                         │          │  CAMADA DE BUSINESS (DOMÍNIO)
=========================│==========│===============================================================
        ▼ manipula       ▼ manipula
    <<entity>>       <<entity>>
      Usuario          Livro
 (Aluno/Professor)
        │                │
====================================================================================================
                              CAMADA DE INFRAESTRUTURA (PERSISTÊNCIA)
====================================================================================================
        ▼ implementa     ▼ implementa
   <<interface>>    <<interface>>
 IUsuarioRepository ILivroRepository
        ▲                ▲
   ┌────┴────┐      ┌────┴────┐
 Memory    Binary Memory    Binary
        ▲                ▲
        └───────┬────────┘
                │ (cria)
       <<Abstract Factory>>
        RepositoryFactory
                ▲
    ┌───────────┴───────────┐
MemoryRepositoryFactory  BinaryRepositoryFactory

====================================================================================================
                                    INFRAESTRUTURA EXTERNA (LOGS)
====================================================================================================
                                         <<interface>>
                                            ILogger
                                               ▲
                                          <<Adapter>>
                                      PythonLoggerAdapter
```

---

## 4. Matriz de Exceções de Domínio

| Exceção | Gatilho de Disparo |
| :--- | :--- |
| `LoginInvalidoException` | Login vazio, com mais de 12 caracteres ou contendo algarismos numéricos. |
| `SenhaFracaException` | Senha com menos de 8 caracteres, sem maiúscula/minúscula/número/símbolo ou igual ao login. |
| `UsuarioDuplicadoException` | Matrícula, e-mail ou login já cadastrados. |
| `LivroInvalidoException` | Campos obrigatórios vazios, ano incoerente, remoção de obra emprestada ou tentativa de desfazer sem atualização prévia. |
| `LivroDuplicadoException` | Tentativa de cadastro de ISBN já existente. |
| `LivroNaoEncontradoException`| Consulta, atualização ou empréstimo referenciando ISBN inexistente. |
| `PersistenciaException` | Falhas de gravação/leitura no arquivo binário (`.bin`). |