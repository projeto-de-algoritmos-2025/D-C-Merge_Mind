"""
Implementação educativa do algoritmo Binary Search
Com visualização e interação para fins didáticos
"""

import copy
from typing import List, Tuple, Optional, Callable
from enum import Enum


class FaseBinarySearch(Enum):
    """Fases do algoritmo Binary Search"""
    INICIALIZACAO = "inicializacao"
    BUSCA = "busca"
    ENCONTRADO = "encontrado"
    NAO_ENCONTRADO = "nao_encontrado"


class BinarySearchEducativo:
    """
    Implementação educativa do Binary Search com suporte a visualização
    e interação do usuário durante o processo de busca
    """
    
    def __init__(self, lista_ordenada: List[int], valor_busca: int, 
                 callback_visual: Optional[Callable] = None):
        self.lista_original = copy.deepcopy(lista_ordenada)
        self.valor_busca = valor_busca
        self.callback_visual = callback_visual
        
        # Estado atual da busca
        self.fase_atual = FaseBinarySearch.INICIALIZACAO
        self.inicio = 0
        self.fim = len(lista_ordenada) - 1
        self.meio = 0
        self.posicao_encontrada = -1
        
        # Estatísticas
        self.comparacoes_realizadas = 0
        self.decisoes_corretas = 0
        self.iteracoes = 0
        
        # Histórico
        self.historico_comparacoes = []
        self.historico_intervalos = []
    
    def inicializar(self) -> None:
        """Inicializa o processo de busca binária"""
        self.fase_atual = FaseBinarySearch.BUSCA
        self.inicio = 0
        self.fim = len(self.lista_original) - 1
        
        # Registrar intervalo inicial
        self.historico_intervalos.append({
            'inicio': self.inicio,
            'fim': self.fim,
            'iteracao': self.iteracoes
        })
        
        if self.callback_visual:
            self.callback_visual('inicializar_busca', {
                'lista': copy.deepcopy(self.lista_original),
                'valor_busca': self.valor_busca,
                'inicio': self.inicio,
                'fim': self.fim
            })
    
    def proximo_passo(self) -> bool:
        """Executa o próximo passo do algoritmo"""
        if self.fase_atual == FaseBinarySearch.INICIALIZACAO:
            self.inicializar()
            return True
            
        elif self.fase_atual == FaseBinarySearch.BUSCA:
            return self._executar_iteracao_busca()
            
        return False
    
    def _executar_iteracao_busca(self) -> bool:
        """Executa uma iteração da busca binária"""
        if self.inicio > self.fim:
            self.fase_atual = FaseBinarySearch.NAO_ENCONTRADO
            
            if self.callback_visual:
                self.callback_visual('valor_nao_encontrado', {
                    'valor_busca': self.valor_busca,
                    'iteracoes': self.iteracoes
                })
            return False
        
        self.meio = (self.inicio + self.fim) // 2
        self.iteracoes += 1
        valor_meio = self.lista_original[self.meio]
        
        # Registrar intervalo atual
        self.historico_intervalos.append({
            'inicio': self.inicio,
            'fim': self.fim,
            'meio': self.meio,
            'valor_meio': valor_meio,
            'iteracao': self.iteracoes
        })
        
        if self.callback_visual:
            self.callback_visual('nova_iteracao', {
                'inicio': self.inicio,
                'fim': self.fim,
                'meio': self.meio,
                'valor_meio': valor_meio,
                'valor_busca': self.valor_busca,
                'iteracao': self.iteracoes
            })
        
        self.comparacoes_realizadas += 1
        
        if valor_meio == self.valor_busca:
            self.posicao_encontrada = self.meio
            self.fase_atual = FaseBinarySearch.ENCONTRADO
            
            if self.callback_visual:
                self.callback_visual('valor_encontrado', {
                    'posicao': self.meio,
                    'valor': valor_meio,
                    'iteracoes': self.iteracoes
                })
            return False
        
        return True
    
    def fazer_decisao_direcao(self, buscar_esquerda: bool) -> Tuple[bool, str]:
        """
        Usuário decide a direção da busca
        
        Args:
            buscar_esquerda: True para buscar na metade esquerda, False para direita
            
        Returns:
            Tuple[bool, str]: (decisao_correta, mensagem_feedback)
        """
        if self.fase_atual != FaseBinarySearch.BUSCA:
            return False, "Não é possível fazer decisão neste momento"
        
        valor_meio = self.lista_original[self.meio]
        
        # Determinar direção correta
        if self.valor_busca < valor_meio:
            direcao_correta = True  # Esquerda
            mensagem_correta = f"{self.valor_busca} < {valor_meio}, buscar à esquerda"
        elif self.valor_busca > valor_meio:
            direcao_correta = False  # Direita
            mensagem_correta = f"{self.valor_busca} > {valor_meio}, buscar à direita"
        else:
            # Valor encontrado, não deveria chegar aqui
            return True, "Valor encontrado!"
        
        decisao_correta = buscar_esquerda == direcao_correta
        
        if decisao_correta:
            self.decisoes_corretas += 1
            mensagem = f"Correto! {mensagem_correta}"
        else:
            mensagem = f"Ops! {mensagem_correta}"
        
        # Registrar comparação
        self.historico_comparacoes.append({
            'valor_meio': valor_meio,
            'valor_busca': self.valor_busca,
            'decisao_usuario': buscar_esquerda,
            'decisao_correta': decisao_correta,
            'iteracao': self.iteracoes
        })
        
        # Atualizar intervalo independentemente da decisão do usuário
        if self.valor_busca < valor_meio:
            self.fim = self.meio - 1
        else:
            self.inicio = self.meio + 1
        
        if self.callback_visual:
            self.callback_visual('decisao_direcao', {
                'decisao_correta': decisao_correta,
                'mensagem': mensagem,
                'novo_inicio': self.inicio,
                'novo_fim': self.fim,
                'valor_meio': valor_meio
            })
        
        return decisao_correta, mensagem
    
    def obter_proxima_comparacao(self) -> Optional[Tuple[int, int, int]]:
        """
        Retorna informações da próxima comparação
        
        Returns:
            Tuple[int, int, int]: (posição_meio, valor_meio, valor_busca) ou None
        """
        if self.fase_atual == FaseBinarySearch.BUSCA and self.inicio <= self.fim:
            meio_temp = (self.inicio + self.fim) // 2
            if meio_temp < len(self.lista_original):
                return (meio_temp, self.lista_original[meio_temp], self.valor_busca)
        return None
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas do processo de busca"""
        total_decisoes = len(self.historico_comparacoes)
        precisao = (self.decisoes_corretas / total_decisoes * 100 
                   if total_decisoes > 0 else 0)
        
        # Calcular complexidade teórica
        import math
        complexidade_teorica = math.ceil(math.log2(len(self.lista_original))) if self.lista_original else 0
        
        return {
            'fase_atual': self.fase_atual.value,
            'iteracoes': self.iteracoes,
            'comparacoes_realizadas': self.comparacoes_realizadas,
            'decisoes_corretas': self.decisoes_corretas,
            'precisao': round(precisao, 2),
            'complexidade_teorica': complexidade_teorica,
            'eficiencia': round((complexidade_teorica / max(self.iteracoes, 1)) * 100, 2),
            'valor_encontrado': self.posicao_encontrada != -1,
            'posicao_encontrada': self.posicao_encontrada if self.posicao_encontrada != -1 else None,
            'esta_completo': self.fase_atual in [FaseBinarySearch.ENCONTRADO, FaseBinarySearch.NAO_ENCONTRADO]
        }
    
    def obter_resultado_final(self) -> Optional[dict]:
        """Retorna o resultado final se a busca estiver completa"""
        if self.fase_atual in [FaseBinarySearch.ENCONTRADO, FaseBinarySearch.NAO_ENCONTRADO]:
            return {
                'encontrado': self.fase_atual == FaseBinarySearch.ENCONTRADO,
                'posicao': self.posicao_encontrada if self.posicao_encontrada != -1 else None,
                'valor_busca': self.valor_busca,
                'iteracoes': self.iteracoes,
                'historico': copy.deepcopy(self.historico_intervalos)
            }
        return None
    
    def reiniciar(self, novo_valor_busca: Optional[int] = None) -> None:
        """Reinicia o algoritmo para uma nova execução"""
        if novo_valor_busca is not None:
            self.valor_busca = novo_valor_busca
        self.__init__(self.lista_original, self.valor_busca, self.callback_visual)
