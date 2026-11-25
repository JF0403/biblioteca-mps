import logging
from abc import ABC, abstractmethod

class ILogger(ABC):
    """Interface alvo esperada pela camada de negócio (Business)."""
    @abstractmethod
    def log_info(self, mensagem: str) -> None:
        pass

    @abstractmethod
    def log_error(self, mensagem: str) -> None:
        pass

class PythonLoggerAdapter(ILogger):
    """Adapter que adapta a biblioteca nativa 'logging' do Python para a interface ILogger."""
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='sistema_biblioteca.log',
            filemode='a'
        )
        self.logger = logging.getLogger("BibliotecaLogger")

    def log_info(self, mensagem: str) -> None:
        self.logger.info(mensagem)

    def log_error(self, mensagem: str) -> None:
        self.logger.error(mensagem)