from typing import Optional
from src.domain.exceptions.livro_exceptions import LivroInvalidoException


class Livro:
    def __init__(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        ano: int,
        matricula_locatario: Optional[str] = None
    ) -> None:
        self._validar(isbn, titulo, autor, ano)
        self.isbn = isbn.strip()
        self.titulo = titulo.strip()
        self.autor = autor.strip()
        self.ano = int(ano)
        self.matricula_locatario = (
            matricula_locatario.strip() if matricula_locatario and matricula_locatario.strip() else None
        )

    @staticmethod
    def _validar(isbn: str, titulo: str, autor: str, ano: int) -> None:
        if not isbn or not str(isbn).strip():
            raise LivroInvalidoException("O ISBN do livro não pode ser vazio.")
        if not titulo or not str(titulo).strip():
            raise LivroInvalidoException("O título do livro não pode ser vazio.")
        if not autor or not str(autor).strip():
            raise LivroInvalidoException("O autor do livro não pode ser vazio.")
        try:
            ano_int = int(ano)
            if ano_int <= 0 or ano_int > 2100:
                raise LivroInvalidoException("O ano de publicação informado é inválido.")
        except (ValueError, TypeError):
            raise LivroInvalidoException("O ano deve ser um valor numérico inteiro.")

    @property
    def esta_emprestado(self) -> bool:
        return self.matricula_locatario is not None

    def associar_locatario(self, matricula: str) -> None:
        if not matricula or not matricula.strip():
            raise LivroInvalidoException("A matrícula do locatário não pode ser vazia.")
        self.matricula_locatario = matricula.strip()

    def desassociar_locatario(self) -> None:
        self.matricula_locatario = None