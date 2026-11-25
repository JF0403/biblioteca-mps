from abc import ABC, abstractmethod
from typing import Dict

class RelatorioEstatisticasTemplate(ABC):
    """Padrão Template Method para geração de relatórios."""
    
    # Este é o Template Method (esqueleto do algoritmo, não pode ser sobrescrito)
    def gerar_relatorio(self, estatisticas: Dict[str, int], caminho_arquivo: str) -> str:
        cabecalho = self._gerar_cabecalho()
        corpo = self._gerar_corpo(estatisticas)
        rodape = self._gerar_rodape()
        
        conteudo_final = f"{cabecalho}\n{corpo}\n{rodape}"
        self._salvar_arquivo(conteudo_final, caminho_arquivo)
        
        return conteudo_final

    @abstractmethod
    def _gerar_cabecalho(self) -> str:
        pass

    @abstractmethod
    def _gerar_corpo(self, estatisticas: Dict[str, int]) -> str:
        pass

    @abstractmethod
    def _gerar_rodape(self) -> str:
        pass

    def _salvar_arquivo(self, conteudo: str, caminho_arquivo: str) -> None:
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)

class RelatorioEstatisticasHTML(RelatorioEstatisticasTemplate):
    def _gerar_cabecalho(self) -> str:
        return "<html>\n<head><title>Relatório de Estatísticas</title></head>\n<body>\n<h2>Relatório de Utilização do Sistema</h2>"

    def _gerar_corpo(self, estatisticas: Dict[str, int]) -> str:
        html = "<ul>\n"
        for chave, valor in estatisticas.items():
            html += f"  <li><b>{chave.capitalize()}:</b> {valor} cadastros ativos</li>\n"
        html += "</ul>"
        return html

    def _gerar_rodape(self) -> str:
        return "</body>\n</html>"

class RelatorioEstatisticasTXT(RelatorioEstatisticasTemplate):
    def _gerar_cabecalho(self) -> str:
        return "========================================\n  RELATÓRIO DE ESTATÍSTICAS DO SISTEMA  \n========================================"

    def _gerar_corpo(self, estatisticas: Dict[str, int]) -> str:
        txt = ""
        for chave, valor in estatisticas.items():
            txt += f"- {chave.capitalize()}: {valor} cadastros ativos\n"
        return txt

    def _gerar_rodape(self) -> str:
        return "========================================"