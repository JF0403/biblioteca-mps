from abc import ABC, abstractmethod
from typing import Any, Optional
from src.infrastructure.adapters.logger_adapter import ILogger


class Command(ABC):
    """Interface Command do padrão GoF."""

    @abstractmethod
    def execute(self) -> Any:
        pass


class CommandInvoker:
    """Invoker (Executor): centraliza a execução e o registro em log dos comandos."""

    def __init__(self, logger: Optional[ILogger] = None) -> None:
        self._logger = logger

    def executar(self, comando: Command) -> Any:
        nome_comando = comando.__class__.__name__
        try:
            resultado = comando.execute()
            if self._logger is not None:
                self._logger.log_info(f"Comando executado com sucesso: {nome_comando}")
            return resultado
        except Exception as erro:
            if self._logger is not None:
                self._logger.log_error(f"Erro ao executar {nome_comando}: {erro}")
            raise