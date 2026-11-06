# Sistema de Gerenciamento de Biblioteca - MPS

Projeto desenvolvido para a disciplina de Métodos de Projeto de Software (UFPB).

## Arquitetura (Padrão BCE)
- Apresentação / Fronteira: Interface de linha de comando interativa (src/presentation/cli.py).
- Aplicação / Controle: Servico de negocio (UsuarioService) e contrato abstrato (IUsuarioRepository).
- Domínio / Entidade: Entidades de negocio (Usuario, Aluno, Professor) e excecoes customizadas.
- Infraestrutura: Persistencia desacoplada em memoria RAM (UsuarioRepositoryMemory).

## Como Executar

Executar a aplicação:
python main.py

Executar os testes automatizados:
python -m unittest discover -s tests

## Documentacao
A especificacao dos Casos de Uso e a analise BCE estao em docs/especificacao.md.