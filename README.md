# Sistema de Gerenciamento de Biblioteca (MPS)

[![Release](https://img.shields.io/badge/release-v3.0.0-blue.svg)](https://github.com/JF0403/biblioteca-mps/releases/tag/v3.0.0)
[![Tests](https://img.shields.io/badge/tests-30%2F30%20passing-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)]()

Projeto prático desenvolvido para a disciplina de Métodos de Projeto de Software (MPS) do Centro de Informática da Universidade Federal da Paraíba (UFPB).

---

## Arquitetura do Sistema (BCE)

O projeto adota estritamente o padrão arquitetural **Boundary-Control-Entity (BCE)**, garantindo baixo acoplamento e separação clara de responsabilidades:

* **Boundary (Fronteira):** Camada de apresentação em linha de comando (`src/presentation/cli.py`), totalmente desacoplada de regras de negócio e persistência.
* **Control (Controlo):**
  * `FacadeSingletonController`: Ponto único de entrada e orquestração para a interface gráfica/CLI.
  * `UsuarioService`: Regras de negócio, unicidade e validações de credenciais.
  * `LivroService`: Gestão do acervo, CRUD e integridade de empréstimos.
* **Entity (Domínio):** Entidades com validações invariantes no construtor:
  * `Usuario` (abstrata), especializada em `Aluno` (limite de 3 livros) e `Professor` (limite de 5 livros).
  * `Livro`: Atributos (`isbn`, `titulo`, `autor`, `ano`, `matricula_locatario`) e controlo de estado de empréstimo.
* **Infraestrutura / Persistência:** Desacoplamento via inversão de dependência (`IUsuarioRepository`, `ILivroRepository`) com implementação dupla:
  * Memória RAM (`UsuarioRepositoryMemory`, `LivroRepositoryMemory`).
  * Ficheiro Binário serializado (`UsuarioRepositoryBinary`, `LivroRepositoryBinary`), com tratamento de exceções de baixo nível (`PersistenciaException`).

---

## Padrões de Projeto (GoF)

1. **Singleton:** A classe `FacadeSingletonController` implementa controlo de instância única global via `__new__` e método `get_instance()`.
2. **Facade:** A mesma classe atua como fachada unificada, reduzindo a complexidade de acesso aos múltiplos subsistemas de serviços.
3. **Repository:** Abstração completa dos mecanismos de armazenamento de dados através de interfaces abstratas.

---

## Validações e Regras de Negócio

* **Validação de Login:** Limite estrito de 12 caracteres, não vazio e proibição de algarismos numéricos (`LoginInvalidoException`).
* **Política de Senha (AWS IAM):** Mínimo de 8 caracteres, exigência de letras maiúsculas, minúsculas, números, caracteres especiais e proibição de senha idêntica ao login (`SenhaFracaException`).
* **Integridade de Acervo:** ISBN único, ano em formato válido e impedimento de remoção de exemplares com empréstimo ativo (`LivroDuplicadoException`, `LivroInvalidoException`, `LivroNaoEncontradoException`).

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

O sistema conta com **30 testes unitários e de integração** implementados com o módulo nativo `unittest`, cobrindo fluxos normais, casos de exceção, limites de validação, isolamento do Singleton e persistência binária em disco:

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
│   │   ├── contracts/
│   │   │   ├── livro_repository.py
│   │   │   └── usuario_repository.py
│   │   └── services/
│   │       ├── facade_singleton_controller.py
│   │       ├── livro_service.py
│   │       └── usuario_service.py
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── livro.py
│   │   │   └── usuario.py
│   │   └── exceptions/
│   │       ├── livro_exceptions.py
│   │       └── usuario_exceptions.py
│   ├── infrastructure/
│   │   ├── binary/
│   │   │   ├── livro_repository_binary.py
│   │   │   └── usuario_repository_binary.py
│   │   └── memory/
│   │       ├── livro_repository_memory.py
│   │       └── usuario_repository_memory.py
│   └── presentation/
│       └── cli.py
├── tests/
│   └── unit/
│       ├── test_facade_singleton_controller.py
│       └── test_usuario_service.py
├── main.py
└── README.md
```

---

## Autoria

* **João Felipe de Araújo Guedes** - Matrícula: 20200007484  
* Universidade Federal da Paraíba (UFPB) - Centro de Informática (CI)