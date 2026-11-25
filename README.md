# Sistema de Gerenciamento de Biblioteca (MPS)

[![Release](https://img.shields.io/badge/release-v5.0.0-blue.svg)](https://github.com/JF0403/biblioteca-mps/releases/tag/v5.0.0)
[![Tests](https://img.shields.io/badge/tests-40%2F40%20passing-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)]()

Projeto prático desenvolvido para a disciplina de Métodos de Projeto de Software (MPS) do Centro de Informática da Universidade Federal da Paraíba (UFPB).

---

## Arquitetura do Sistema (BCE)

O projeto adota estritamente o padrão arquitetural **Boundary-Control-Entity (BCE)**, garantindo baixo acoplamento e separação clara de responsabilidades:

* **Boundary (Fronteira):** Camada de apresentação em linha de comando (`src/presentation/cli.py`), totalmente desacoplada de regras de negócio e persistência.
* **Control (Controle):**
  * `FacadeSingletonController`: Ponto único de entrada e orquestração da camada de negócio, delegando todas as operações ao `CommandInvoker`.
  * `UsuarioService`: Regras de negócio, unicidade e validações de credenciais.
  * `LivroService`: Gestão do acervo, CRUD e integridade de empréstimos.
* **Entity (Domínio):** Entidades com validações invariantes no construtor:
  * `Usuario` (abstrata), especializada em `Aluno` (limite de 3 livros) e `Professor` (limite de 5 livros).
  * `Livro`: Atributos (`isbn`, `titulo`, `autor`, `ano`, `matricula_locatario`) e controle de estado de empréstimo.
* **Infraestrutura / Persistência:** Desacoplamento via inversão de dependência (`IUsuarioRepository`, `ILivroRepository`) com criação centralizada por fábricas abstratas (`RepositoryFactory`):
  * Memória RAM (`UsuarioRepositoryMemory`, `LivroRepositoryMemory`).
  * Arquivo Binário serializado (`UsuarioRepositoryBinary`, `LivroRepositoryBinary`), com tratamento de exceções de baixo nível (`PersistenciaException`).

---

## Padrões de Projeto (GoF) Implementados

1. **Singleton:** `FacadeSingletonController` garante instância única global via `__new__` e `get_instance()`.
2. **Facade:** `FacadeSingletonController` oferece uma interface unificada para todos os subsistemas de negócio.
3. **Repository:** Abstração dos mecanismos de persistência por meio das interfaces `IUsuarioRepository` e `ILivroRepository`.
4. **Abstract Factory:** `RepositoryFactory` (`MemoryRepositoryFactory` e `BinaryRepositoryFactory`) isola a instanciação das famílias de repositórios.
5. **Adapter:** `PythonLoggerAdapter` adapta a biblioteca nativa `logging` do Python para a interface de domínio `ILogger`.
6. **Template Method:** `RelatorioEstatisticasTemplate` define o esqueleto de geração de relatórios de estatísticas, especializado em `RelatorioEstatisticasHTML` e `RelatorioEstatisticasTXT`.
7. **Command:** `Command`, `CommandInvoker` e os comandos concretos em `biblioteca_commands.py` encapsulam cada operação invocada pela fachada, centralizando execução e auditoria em log.
8. **Memento:** `LivroOriginator`, `LivroMemento` e `LivroCaretaker` armazenam um snapshot imutável antes de cada atualização de `Livro`, permitindo desfazer a última edição realizada.

---

## Diagrama de Classes (Visão Geral BCE + GoF)

```text
[UserCLI <<boundary>>] ──▶ [FacadeSingletonController <<Singleton, Facade>>]
                                  │
                                  ├──▶ [CommandInvoker] ──▶ [Command <<interface>>]
                                  │                              ├── CadastrarUsuarioCommand
                                  │                              ├── AtualizarLivroCommand ──▶ [LivroOriginator] ──▶ [LivroMemento]
                                  │                              ├── DesfazerUltimaAtualizacaoLivroCommand ──▶ [LivroCaretaker]
                                  │                              └── ExportarRelatorioEstatisticasCommand ──▶ [RelatorioEstatisticasTemplate]
                                  │
                                  └──▶ [ILogger <<Adapter>>] ◀── [PythonLoggerAdapter]

[UsuarioService / LivroService] ──▶ [IUsuarioRepository / ILivroRepository] ◀── [RepositoryFactory <<Abstract Factory>>]
```

*(O diagrama estrutural completo encontra-se em `docs/especificacao.md`.)*

---

## Validações e Regras de Negócio

* **Validação de Login:** Limite estrito de 12 caracteres, não vazio e proibição de algarismos numéricos (`LoginInvalidoException`).
* **Política de Senha (AWS IAM):** Mínimo de 8 caracteres, exigência de letras maiúsculas, minúsculas, números, caracteres especiais e proibição de senha idêntica ao login (`SenhaFracaException`).
* **Integridade de Acervo:** ISBN único, ano em formato válido, impedimento de remoção de exemplares com empréstimo ativo e restauração de estado via Memento (`LivroDuplicadoException`, `LivroInvalidoException`, `LivroNaoEncontradoException`).

---

## Execução da Aplicação

Para iniciar o sistema interativo via terminal:

```cmd
python main.py
```

No menu inicial, selecione o mecanismo de persistência pretendido:
* `1` - Coleção em Memória RAM
* `2` - Arquivo Binário (`.bin`)

---

## Suíte de Testes Automatizados

O sistema conta com **40 testes unitários e de integração** implementados com o módulo nativo `unittest`, cobrindo regras de domínio, limites de validação, isolamento do Singleton, persistência binária, Abstract Factory, Adapter, Template Method, Command e Memento:

```cmd
python -m unittest discover -s tests
```

---

## Estrutura do Repositório

```text
biblioteca-mps/
├── docs/
│   └── especificacao.md
├── src/
│   ├── application/
│   │   ├── commands/
│   │   │   ├── biblioteca_commands.py
│   │   │   └── command.py
│   │   ├── contracts/
│   │   │   ├── livro_repository.py
│   │   │   └── usuario_repository.py
│   │   ├── memento/
│   │   │   └── livro_memento.py
│   │   └── services/
│   │       ├── facade_singleton_controller.py
│   │       ├── livro_service.py
│   │       ├── relatorio_template.py
│   │       └── usuario_service.py
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── livro.py
│   │   │   └── usuario.py
│   │   └── exceptions/
│   │       ├── livro_exceptions.py
│   │       └── usuario_exceptions.py
│   ├── infrastructure/
│   │   ├── adapters/
│   │   │   └── logger_adapter.py
│   │   ├── binary/
│   │   │   ├── livro_repository_binary.py
│   │   │   └── usuario_repository_binary.py
│   │   ├── factories/
│   │   │   └── repository_factory.py
│   │   └── memory/
│   │       ├── livro_repository_memory.py
│   │       └── usuario_repository_memory.py
│   └── presentation/
│       └── cli.py
├── tests/
│   └── unit/
│       ├── test_facade_singleton_controller.py
│       ├── test_sprint4_padroes.py
│       ├── test_sprint5_command_memento.py
│       └── test_usuario_service.py
├── main.py
└── README.md
```

---

